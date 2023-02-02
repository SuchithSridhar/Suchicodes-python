
function get_category_html(css_class, id, name, uuid) {
    return (
        `
        <li>
            <a class='${css_class}' href="#category-${id}" role="button"
                aria-expanded="false" aria-controls="collapseExample" data-bs-toggle="collapse">
                <i class="list-style fas fa-angle-right"></i>
                ${name}
            </a>
            <ul id='category-${id}' data-category-id='${id}' class="list collapse"></ul>
        </li>

        `
    )
}

function setCategories(categories){
    let top_level = $('#top-level-list');
    let parent = null;
    let html = '';
    let top_level_css_class = 'upper-list-header'
    let list_level_css_class = 'list-header'

    categories.forEach(item => {
        if (item.name != "deleted" && item.parent == 0) {
           html = top_level.html();
           top_level.html(
               html +
               get_category_html(top_level_css_class, item.id, item.name, item.uuid)
           );
        }
    });
    categories.forEach(item => {
        if (item.parent != 0) {
           parent = $(`#category-${item.parent}`);
           html = parent.html();
           parent.html(
               html +
               get_category_html(list_level_css_class, item.id, item.name, item.uuid)
           );
        }
    });
}

function setBlogs(blogs){
    let parent = null;
    let html = '';
    let deleted_category_id = 999999;

    blogs.forEach(item => {
        // ignore blogs in deleted category
        if (item.category == deleted_category_id) return;

        parent = $('ul').find(`[data-category-id='${item.category}']`);
        html = parent.html();
        parent.html(html + 
        `<li>
            <a class='list-blog'
                href="/resources/blog/${item.id.slice(0, 8)}">
                <i class="list-style fas fa-caret-right"></i>
                ${item.title}
            </a>
        </li>`);

    });
}
