function resetFilters() {
    const filtersWidget = document.getElementById('filters-widget');
    const form = filtersWidget.querySelector('#filter-form');

    const filterElements = form.querySelectorAll('p');

    filterElements.forEach(element => {
        const label = element.querySelector('label');
        if (label) {
            const inputId = label.getAttribute('for');
            const input = form.querySelector(`#${inputId}`);
            input.value = null;
        }
    });
    form.submit();
}

document.addEventListener('DOMContentLoaded', function() {
    const filtersWidget = document.getElementById('filters-widget');
    const form = filtersWidget.querySelector('#filter-form');
    const filterElements = form.querySelectorAll('p');

    const select = document.createElement('select');

    filterElements.forEach(element => {
        const label = element.querySelector('label');
        if (label) {
            const inputId = label.getAttribute('for');
            const input = form.querySelector(`#${inputId}`);
            /* Some inputs on form located in separated <p>
            *  and there we concat them to their label <p> 
            *  and removing old <p>
            */
            if(input) {  
                if(!label.parentElement.isEqualNode(input.parentElement)) {
                    const oldParent = input.parentElement;
                    label.parentElement.appendChild(input);
                    oldParent.remove();
                }
            }

            label.style.display = 'none'; // removing label

            /*Creating select options for filters*/
            const option = document.createElement('option');
            option.text = label.textContent.trim().replace(/.$/, "");
            option.value = label.getAttribute('for');
            select.appendChild(option);
        }
    });

    select.addEventListener('change', function() {
        const selectedFilterId = this.value;

        filterElements.forEach(element => {  
            const label = element.querySelector('label');
            element.style.display = 'none'; // hiding all filters
            if(label) {
                const inputId = label.getAttribute('for');
                if (inputId === selectedFilterId) { 
                    element.style.display = 'inline'; // showing only selected filter
                    localStorage.setItem(`${window.location.pathname}/selected_filter`, selectedFilterId); // saving current selected filter

                }
            }
        });
    });
    /* restoring selected filter */
    const selectedFilter = localStorage.getItem(`${window.location.pathname}/selected_filter`);
    if(selectedFilter) { 
        select.value = selectedFilter;
    }
    select.dispatchEvent(new Event('change'));

    filtersWidget.insertBefore(select, form);

    return true;
});
