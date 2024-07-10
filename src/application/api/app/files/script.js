document.addEventListener('DOMContentLoaded', () => {
    let categories = {};
    const todoListElement = document.getElementById('todo-list');
    const todoCountElement = document.getElementById('todo-count');
    const newTodoInput = document.getElementById('new-todo');
    const addTodoButton = document.getElementById('add-todo');
    const newCategoryInput = document.getElementById('new-category');
    const addCategoryButton = document.getElementById('add-category');
    const categoryListElement = document.getElementById('category-list');
    const deadlineInput = document.getElementById('deadline');
    const categorySelect = document.getElementById('category-select');
    const registerEmailInput = document.getElementById('register-email');
    const registerPasswordInput = document.getElementById('register-password');
    const registerButton = document.getElementById('register-button');
    const loginEmailInput = document.getElementById('login-email');
    const loginPasswordInput = document.getElementById('login-password');
    const loginButton = document.getElementById('login-button');
    const authContainer = document.getElementById('auth-container');
    const todoApp = document.getElementById('todo-app');
    const showRegisterLink = document.getElementById('show-register');
    const showLoginLink = document.getElementById('show-login');
    const logoutButton = document.getElementById('logout-button')

    registerButton.addEventListener('click', register);
    loginButton.addEventListener('click', login);
    addTodoButton.addEventListener('click', addTodo);
    addCategoryButton.addEventListener('click', addCategory);
    showRegisterLink.addEventListener('click', showRegisterForm);
    showLoginLink.addEventListener('click', showLoginForm);
    logoutButton.addEventListener('click', logOut);

    async function renderTodos() {
        todoListElement.innerHTML = '';
        let response = await fetch('http://localhost:80/task/get-all', {
            method: 'get'
        });
        if (!response.ok) {
            showLoginForm();
        } else {
            const userTodos = (await response.json()).tasks;
            todoCountElement.textContent = userTodos.length;
            userTodos.forEach(todo => {
                const li = document.createElement('li');
                li.dataset.taskId = todo.oid;  // Добавляем data-атрибут для идентификации

                const taskText = document.createElement('span');
                taskText.textContent = todo.name;
                li.appendChild(taskText);

                if (todo.deadline) {
                    const now = new Date();
                    const deadline = new Date(todo.deadline);
                    const deadlineText = document.createElement('span');
                    deadlineText.textContent = `${deadline.toLocaleString()}`;
                    if (deadline < now && !todo.is_complete) {
                        li.classList.add('overdue');
                    }
                    li.appendChild(deadlineText);
                }

                if (todo.category_oid) {
                    const categoryTitle = categories[todo.category_oid] || 'Неизвестная категория';
                    const categoryText = document.createElement('span');
                    categoryText.textContent = `${categoryTitle}`;
                    li.appendChild(categoryText);
                }

                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.checked = todo.is_complete;
                checkbox.addEventListener('change', () => {
                    if (checkbox.checked) {
                        toggleComplete(todo.oid);
                    } else {
                        toggleUnComplete(todo.oid);
                    }
                });
                li.appendChild(checkbox);

                const editButton = document.createElement('button');
                editButton.textContent = 'Редактировать'
                editButton.addEventListener('click', () => showEditForm(todo.oid, todo.name, categories[todo.category_oid], todo.deadline));
                li.appendChild(editButton);

                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Удалить';
                deleteButton.addEventListener('click', () => deleteTodo(todo.oid));
                li.appendChild(deleteButton);

                todoListElement.appendChild(li);
            });
        }
    }

    async function renderCategories() {
    categoryListElement.innerHTML = '';
    let response = await fetch('http://localhost:80/category/get-all', {
        method: 'get'
    });
    if (!response.ok) {
        showLoginForm()
    } else {
        const data = await response.json();
        data.categories.forEach(category => {
            categories[category.oid] = category.title; // Записываем в объект categories
            const li = document.createElement('li');
            li.textContent = category.title;

            const editButton = document.createElement('button');
            editButton.textContent = 'Редактировать'
            editButton.addEventListener('click', () => editCategory(category.oid, category.title));

            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Удалить';
            deleteButton.addEventListener('click', () => deleteCategory(category.oid));

            li.appendChild(editButton);
            li.appendChild(deleteButton);
            categoryListElement.appendChild(li);
        });
        updateCategorySelect();
    }
}

    async function addTodo() {
    const text = newTodoInput.value.trim();
    const deadline = deadlineInput.value;
    const category = categorySelect.value;

    if (text) {
        const response = await fetch('http://localhost:80/task/create', {
            method: 'post',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: text,
                deadline: deadline ? new Date(deadline).toISOString() : null,
                category_oid: category || null
            })
        });

        if (response.ok) {
            newTodoInput.value = '';
            deadlineInput.value = '';
            categorySelect.selectedIndex = 0;
            await renderTodos();
        } else {
            alert((await response.json()).detail.error);
        }
    } else {
        alert('Пожалуйста, введите описание задачи.');
    }
}

    async function showEditForm(taskId, currentText, currentCategory, currentDeadline) {
        const editForm = document.createElement('form');
        editForm.innerHTML = `
            <input type="text" id="edit-text" value="${currentText}">
            <select id="edit-category">
                <option value="">Без категории</option>
                ${Object.keys(categories).map(oid => `
                    <option value="${oid}" ${oid === currentCategory ? 'selected' : ''}>${categories[oid]}</option>
                `).join('')}
            </select>
            <input type="datetime-local" id="edit-deadline" value="${currentDeadline ? currentDeadline.slice(0, 16) : ''}">
            <button type="submit">Сохранить</button>
            <button type="button" id="cancel-edit">Отмена</button>
        `;

        const cancelButton = editForm.querySelector('#cancel-edit');
        cancelButton.addEventListener('click', () => {
            editForm.remove();
            renderTodos();
        });

        editForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const newText = editForm.querySelector('#edit-text').value.trim();
            const newCategory = editForm.querySelector('#edit-category').value;
            const newDeadline = editForm.querySelector('#edit-deadline').value;

            if (newText) {
                const response = await fetch('http://localhost:80/task/update/', {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        task_oid: taskId,
                        name: newText,
                        category_oid: newCategory || null,
                        deadline: newDeadline ? new Date(newDeadline).toISOString() : null
                    })
                });
                if (response.ok) {
                    await renderTodos();
                } else {
                    alert((await response.json()).detail.error);
                }
            } else {
                alert('Описание задачи не может быть пустым.');
            }
        });

        const todoItem = document.querySelector(`li[data-task-id="${taskId}"]`);
        if (todoItem) {
            todoItem.innerHTML = '';
            todoItem.appendChild(editForm);
        } else {
            alert('Задача не найдена');
        }
    }

    async function editCategory(categoryId, currentTitle) {
    const newTitle = prompt('Введите новое название категории:', currentTitle);
    if (newTitle) {
        const response = await fetch('http://localhost:80/category/update/', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ category_oid: categoryId, title: newTitle })
        });
        if (response.ok) {
            await renderCategories();
            await renderTodos();
        } else if (response.status === 401) {
            alert((await response.json()).detail.error);
            showLoginForm();
        } else {
            alert((await response.json()).detail.error);
        }
    }
}

    async function deleteCategory(categoryId) {
        const response = await fetch('http://localhost:80/category/delete/', {
            method: 'DELETE',
            headers: {
                    'Content-Type': 'application/json'
                },
            body: JSON.stringify({ category_oid: categoryId })
        });
        if (response.ok) {
            await renderCategories();
            await renderTodos();
        } else {
            alert((await response.json()).detail.error);
        }
    }

    async function addCategory() {
        const title = newCategoryInput.value.trim();
        if (title) {
            const response = await fetch('http://localhost:80/category/create', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title: title })
            });
            if (response.ok) {
                newCategoryInput.value = '';
                await renderCategories();
            } else {
                alert((await response.json()).detail.error);
            }
        } else {
            alert('Пожалуйста, введите название категории.');
        }
    }

    function updateCategorySelect() {
        categorySelect.innerHTML = '<option value="" disabled selected>Выберите категорию</option>';
        Object.keys(categories).forEach(oid => {
            const option = document.createElement('option');
            option.value = oid;
            option.textContent = categories[oid];
            categorySelect.appendChild(option);
        });
    }

    function isValidDate(dateString) {
        const date = new Date(dateString);
        return !isNaN(date.getTime());
    }

    async function toggleComplete(taskId) {
        const response = await fetch('http://localhost:80/task/complete/', {
            method: 'PATCH',
            headers: {
                    'Content-Type': 'application/json'
                },
            body: JSON.stringify({ task_oid: taskId })
        });
        if (response.ok) {
            await renderTodos();
        } else {
            alert((await response.json()).detail.error);
        }
    }

    async function toggleUnComplete(taskId) {
        const response = await fetch('http://localhost:80/task/uncomplete/', {
            method: 'PATCH',
            headers: {
                    'Content-Type': 'application/json'
                },
            body: JSON.stringify({ task_oid: taskId })
        });
        if (response.ok) {
            await renderTodos();
        } else {
            alert((await response.json()).detail.error);
        }
    }

    async function deleteTodo(taskId) {
        const response = await fetch('http://localhost:80/task/delete/', {
            method: 'DELETE',
            headers: {
                    'Content-Type': 'application/json'
                },
            body: JSON.stringify({ task_oid: taskId })
        });
        if (response.ok) {
            await renderTodos();
        } else {
            alert((await response.json()).detail.error);
        }
    }

    async function register() {
        const email = registerEmailInput.value.trim();
        const password = registerPasswordInput.value.trim();
        if (email && password) {
            const response = await fetch('http://localhost:80/user/sign-up', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            if (response.ok) {
                alert('Регистрация успешна. Пожалуйста, войдите.');
                showLoginForm();
            } else {
                alert((await response.json()).detail.error);
            }
        } else {
            alert('Пожалуйста, заполните все поля.');
        }
    }

    async function login() {
        const email = loginEmailInput.value.trim();
        const password = loginPasswordInput.value.trim();
        if (email && password) {
            const response = await fetch('http://localhost:80/user/sign-in', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            if (response.ok) {
                localStorage.setItem('auth', 'true')
                authContainer.style.display = 'none';
                todoApp.style.display = 'block';
                await renderCategories();
                await renderTodos();
            } else {
                localStorage.setItem('auth', 'false')
                alert((await response.json()).detail.error);
            }
        } else {
            alert('Пожалуйста, заполните все поля.');
        }
    }

    function showLoginForm() {
        authContainer.style.display = 'block';
        document.getElementById('register-form').style.display = 'none';
        document.getElementById('login-form').style.display = 'block';
        todoApp.style.display = 'none';
    }

    function showRegisterForm() {
            authContainer.style.display = 'block';
            document.getElementById('register-form').style.display = 'block';
            document.getElementById('login-form').style.display = 'none';
            todoApp.style.display = 'none';
        }

    function logOut(){
        localStorage.removeItem('auth')
        showLoginForm()
    }

    if (localStorage.getItem('auth')){
        authContainer.style.display = 'none';
        todoApp.style.display = 'block';
        renderCategories();
        renderTodos();
    }else {
        showLoginForm()
    }
});