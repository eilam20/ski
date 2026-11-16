function initAsyncOrderForm(formSelector) {
    const form = document.querySelector(formSelector);
    if (!form) return;

    const submitBtn = form.querySelector('button[type="submit"]');
    const statusBox = document.getElementById('form-status-alert');
    const allowAddAnother = form.dataset.allowAddAnother === 'true';
    const originalBtnText = submitBtn ? submitBtn.textContent : '';

    function showStatus(type, html) {
        if (!statusBox) return;
        statusBox.className = `alert alert-${type} mt-3`;
        statusBox.innerHTML = html;
        statusBox.style.display = 'block';
        statusBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function clearFieldErrors() {
        form.querySelectorAll('.async-field-error').forEach(el => el.remove());
    }

    function renderFieldErrors(errors) {
        const summaryItems = [];
        for (const [fieldName, messages] of Object.entries(errors)) {
            const text = Array.isArray(messages) ? messages.join(', ') : String(messages);
            summaryItems.push(`<li>${text}</li>`);
            const input = form.querySelector(`[name="${fieldName}"]`);
            if (input) {
                const errEl = document.createElement('div');
                errEl.className = 'async-field-error text-danger small mt-1';
                errEl.textContent = text;
                input.insertAdjacentElement('afterend', errEl);
            }
        }
        return summaryItems.length ? `<ul class="mb-0 mt-1">${summaryItems.join('')}</ul>` : '';
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        clearFieldErrors();

        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'שומר...';
        }
        showStatus('info', '<strong>שולח בקשה לשרת...</strong> אנא המתן.');

        try {
            const response = await fetch(form.action || window.location.href, {
                method: 'POST',
                body: new FormData(form),
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const contentType = response.headers.get('content-type') || '';
            if (!contentType.includes('application/json')) {
                throw new Error(`תגובה לא צפויה מהשרת (קוד ${response.status})`);
            }

            const data = await response.json();

            if (response.ok && data.success) {
                const o = data.order || {};
                const details = [
                    o.id ? `מס׳ #${o.id}` : '',
                    o.name ? `שם: ${o.name}` : '',
                    o.phone ? `טלפון: ${o.phone}` : '',
                    o.return_date ? `החזרה: ${o.return_date}` : ''
                ].filter(Boolean).join(' | ');

                if (allowAddAnother) {
                    showStatus(
                        'success',
                        `<strong>${data.message}</strong>` +
                        (details ? `<div class="mt-1">${details}</div>` : '') +
                        `<div class="mt-3 d-flex gap-2 flex-wrap">` +
                        `<button type="button" id="add-another-order-btn" class="btn btn-primary btn-sm">הוסף הזמנה נוספת</button>` +
                        `<a href="${data.redirect_url || '/'}" class="btn btn-secondary btn-sm">חזרה לדף הבית</a>` +
                        `</div>`
                    );

                    const addAnotherBtn = document.getElementById('add-another-order-btn');
                    if (addAnotherBtn) {
                        addAnotherBtn.addEventListener('click', () => {
                            form.reset();
                            clearFieldErrors();
                            if (statusBox) statusBox.style.display = 'none';
                            if (submitBtn) {
                                submitBtn.disabled = false;
                                submitBtn.textContent = originalBtnText;
                            }
                            const firstInput = form.querySelector('input, select, textarea');
                            if (firstInput) firstInput.focus();
                        });
                    }
                    return;
                }

                showStatus(
                    'success',
                    `<strong>${data.message}</strong>` +
                    (details ? `<div class="mt-1">${details}</div>` : '') +
                    `<div class="mt-1 small">מעביר לדף הבית...</div>`
                );

                setTimeout(() => {
                    window.location.href = data.redirect_url || '/';
                }, 900);
                return;
            }

            const errorList = data.errors ? renderFieldErrors(data.errors) : '';
            showStatus('danger', `<strong>${data.message || 'שגיאה בשמירת ההזמנה.'}</strong>${errorList}`);
        } catch (err) {
            showStatus(
                'danger',
                `<strong>הבקשה נכשלה:</strong> ${err.message || 'בעיית תקשורת עם השרת'}. ההזמנה לא נשמרה — אפשר לנסות שוב.`
            );
        } finally {
            if (submitBtn && (!statusBox || !statusBox.classList.contains('alert-success'))) {
                submitBtn.disabled = false;
                submitBtn.textContent = originalBtnText;
            }
        }
    });
}

