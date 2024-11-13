document.addEventListener("DOMContentLoaded", async () => {
  const response = await fetch("/tasks");
  const tasks = await response.json();

  const columns = {
    "To Do": document.querySelector("#to-do .tasks"),
    "In Progress": document.querySelector("#in-progress .tasks"),
    Done: document.querySelector("#done .tasks"),
  };

  tasks.forEach((task) => {
    const taskElement = document.createElement("div");
    taskElement.classList.add("task");

    taskElement.innerHTML = `
            <h3>${task.name}</h3>
            <p>${task.description}</p>
            <p class="priority">Priority: ${task.priority}</p>
            <p>Assignee: ${task.assignee || "Unassigned"}</p>
        `;

    columns[task.status].appendChild(taskElement);
  });
});
