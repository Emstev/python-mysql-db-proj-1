<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Cloudboosta Flask REST API UI</title>
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      background: linear-gradient(to right, #fceabb, #f8b500);
      color: #333;
      padding: 20px;
      max-width: 800px;
      margin: auto;
    }

    h1, h2 {
      text-align: center;
      color: #2c3e50;
    }

    #alertBox {
      display: none;
      padding: 12px;
      border-radius: 8px;
      margin-bottom: 15px;
      text-align: center;
      font-weight: bold;
      transition: opacity 0.5s ease;
    }

    #loadingSpinner {
      display: none;
      text-align: center;
      font-style: italic;
      color: #555;
      margin-top: 10px;
    }

    form {
      background-color: #fffbe6;
      padding: 20px;
      border-radius: 12px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
      margin-bottom: 30px;
    }

    label {
      display: block;
      margin-top: 10px;
      font-weight: bold;
    }

    input[type="text"],
    input[type="email"] {
      width: 100%;
      padding: 10px;
      margin-top: 5px;
      margin-bottom: 15px;
      border-radius: 6px;
      border: 1px solid #ccc;
    }

    button {
      padding: 10px 20px;
      margin-top: 10px;
      margin-right: 10px;
      border: none;
      border-radius: 6px;
      font-weight: bold;
      cursor: pointer;
      transition: all 0.3s ease;
    }

    button:hover {
      opacity: 0.9;
      transform: scale(1.03);
    }

    button[type="button"] {
      background-color: #27ae60;
      color: white;
    }

    #cancelUpdate {
      background-color: #c0392b;
      color: white;
    }

    ul#dataList {
      list-style: none;
      padding: 0;
    }

    ul#dataList li {
      background-color: #ffffff;
      margin-bottom: 12px;
      padding: 15px;
      border-radius: 8px;
      box-shadow: 0 1px 6px rgba(0, 0, 0, 0.1);
    }

    ul#dataList li button {
      margin-top: 10px;
      margin-right: 5px;
      padding: 6px 12px;
      font-size: 0.9rem;
      border-radius: 5px;
    }

    ul#dataList li .edit-btn {
      background-color: #3498db;
      color: white;
    }

    ul#dataList li .delete-btn {
      background-color: #e74c3c;
      color: white;
    }
  </style>
</head>
<body>
  <h1>Cloudboosta Flask REST API UI</h1>
  <h2 id="formTitle">Insert Record</h2>

  <div id="alertBox"></div>
  <div id="loadingSpinner">⏳ Please wait...</div>

  <form id="recordForm">
    <input type="hidden" id="recordId" />
    <label for="name">Name:</label>
    <input type="text" id="name" required />

    <label for="email">Email:</label>
    <input type="email" id="email" />

    <label for="status">Status:</label>
    <input type="text" id="status" />

    <button type="button" onclick="submitForm()">Submit</button>
    <button type="button" id="cancelUpdate" onclick="resetForm()" style="display:none;">Cancel</button>
  </form>

  <h2>All Records</h2>
  <ul id="dataList"></ul>

  <script>
    function showAlert(message, type = "success") {
      const alertBox = document.getElementById('alertBox');
      alertBox.style.display = 'block';
      alertBox.style.backgroundColor = type === "success" ? "#2ecc71" : "#e74c3c";
      alertBox.style.color = "white";
      alertBox.innerText = message;
      alertBox.style.opacity = 1;
      setTimeout(() => {
        alertBox.style.opacity = 0;
        setTimeout(() => alertBox.style.display = 'none', 300);
      }, 3000);
    }

    function showLoading(show) {
      const spinner = document.getElementById('loadingSpinner');
      spinner.style.display = show ? 'block' : 'none';
    }

    function submitForm() {
      const id = document.getElementById('recordId').value;
      const name = document.getElementById('name').value.trim();
      const email = document.getElementById('email').value.trim();
      const status = document.getElementById('status').value.trim();

      if (!name) {
        showAlert('Name is required.', 'error');
        return;
      }

      const payload = JSON.stringify({ name, email, status });
      const url = id ? `/update_record/${id}` : '/insert_record';
      const method = id ? 'PUT' : 'POST';

      showLoading(true);
      fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: payload
      })
      .then(res => res.json())
      .then(data => {
        showAlert(data.message || data.error, data.error ? 'error' : 'success');
        resetForm();
        loadData();
      })
      .catch(() => {
        showAlert('Network error. Please try again.', 'error');
      })
      .finally(() => showLoading(false));
    }

    function loadData() {
      fetch('/data')
        .then(res => res.json())
        .then(data => {
          const dataList = document.getElementById('dataList');
          dataList.innerHTML = '';
          data.forEach(record => {
            const li = document.createElement('li');
            li.innerHTML = `
              <strong>ID:</strong> ${record.id}<br>
              <strong>Name:</strong> ${record.name}<br>
              <strong>Email:</strong> ${record.email || 'N/A'}<br>
              <strong>Status:</strong> ${record.status || 'N/A'}<br>
              <button class="edit-btn" onclick="editRecord(${record.id}, '${record.name}', '${record.email || ''}', '${record.status || ''}')">Edit</button>
              <button class="delete-btn" onclick="deleteRecord(${record.id})">Delete</button>
            `;
            dataList.appendChild(li);
          });
        });
    }

    function editRecord(id, name, email, status) {
      document.getElementById('recordId').value = id;
      document.getElementById('name').value = name;
      document.getElementById('email').value = email;
      document.getElementById('status').value = status;
      document.getElementById('formTitle').innerText = 'Update Record';
      document.getElementById('cancelUpdate').style.display = 'inline';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function deleteRecord(id) {
      if (!confirm(`Are you sure you want to delete record ID ${id}?`)) return;

      showLoading(true);
      fetch(`/delete_record/${id}`, {
        method: 'DELETE'
      })
      .then(res => res.json())
      .then(data => {
        showAlert(data.message || data.error, data.error ? 'error' : 'success');
        loadData();
      })
      .catch(() => {
        showAlert('Failed to delete. Try again.', 'error');
      })
      .finally(() => showLoading(false));
    }

    function resetForm() {
      document.getElementById('recordId').value = '';
      document.getElementById('name').value = '';
      document.getElementById('email').value = '';
      document.getElementById('status').value = '';
      document.getElementById('formTitle').innerText = 'Insert Record';
      document.getElementById('cancelUpdate').style.display = 'none';
    }

    window.onload = loadData;
  </script>
</body>
</html>
