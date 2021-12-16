
function setCategories(categories){
    let top_level = $('#top-level-list');
    let parent = null;
    let html = '';

    categories.forEach(item => {
        if (item.category != "deleted" && item.parent == 0) {
           html = top_level.html();
           top_level.html(html +
               `<li>
                    <a class='upper-list-header' href="#category-${item.id}" role="button"
                        aria-expanded="false" aria-controls="collapseExample" data-bs-toggle="collapse">
                        <i class="list-style fas fa-angle-right"></i>
                        ${item.category}
                    </a>
                    <ul id='category-${item.id}' class="list collapse"></ul>
                </li>`);
        }
    });
    categories.forEach(item => {
        if (item.parent != 0) {
           parent = $(`#category-${item.parent}`);
           html = parent.html();
           parent.html(html + 
            `<li>
                <a class='list-header' data-bs-toggle="collapse" role="button"
                    aria-expanded="false" aria-controls="collapseExample" href="#category-${item.id}">
                    <i class="list-style fas fa-angle-right"></i>
                    ${item.category}
                </a>
                <ul class="collapse list" id='category-${item.id}'></ul>
            </li>`);
        }
    });
}

function setBlogs(blogs){
    let parent = null;
    let html = '';

    console.log(blogs);
    blogs.forEach(item => {
        parent = $(`#category-${item.category}`);
        html = parent.html();
        parent.html(html + 
        `<li>
            <a class='list-blog'
                href="/resources/blog/${item.id}">
                <i class="list-style fas fa-caret-right"></i>
                ${item.title}
            </a>
        </li>`);

    });
}