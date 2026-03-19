import os

BASE_DIR = r"c:\Users\Acer\Desktop\GlobalVision\globalvision"

files_to_write = {}

files_to_write["templates/auth/admin_login.html"] = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login - PeakRent</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/admin_login.css' %}">
</head>
<body>
    <div class="login-card">
        <h1 class="logo">Peak<span>Rent</span></h1>
        <div class="portal-label">Admin Portal</div>
        
        {% if error %}
        <div class="error-message">
            {{ error }}
        </div>
        {% endif %}

        <form method="POST">
            {% csrf_token %}
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="btn-submit">Sign In</button>
        </form>
    </div>
</body>
</html>
"""

files_to_write["templates/dashboard/base_dashboard.html"] = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Dashboard{% endblock %} - PeakRent Admin</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/dashboard.css' %}">
</head>
<body>
    <!-- Sidebar -->
    <aside class="sidebar">
        <div class="sidebar-logo">Peak<span>Rent</span></div>
        
        <div class="nav-section-label">Overview</div>
        <a href="{% url 'dashboard_home' %}" class="nav-link">Dashboard</a>
        
        <div class="nav-section-label">Content</div>
        <a href="{% url 'vehicle_list' %}" class="nav-link">Vehicles</a>
        <a href="{% url 'equipment_list' %}" class="nav-link">Equipment</a>
        <a href="#" class="nav-link">Bookings</a>
        <a href="{% url 'blog_list' %}" class="nav-link">Blog Posts</a>
        
        <div class="nav-section-label">Pages</div>
        <a href="{% url 'about_editor' %}" class="nav-link">About Us</a>
        <a href="{% url 'contact_editor' %}" class="nav-link">Contact Us</a>

        <div class="sidebar-bottom">
            <div class="avatar">{{ request.user.username|make_list|first|upper }}</div>
            <div>
                <div class="admin-name">{{ request.user.username }}</div>
                <a href="{% url 'admin_logout' %}" class="logout-link">Log out</a>
            </div>
        </div>
    </aside>

    <!-- Topbar -->
    <header class="topbar">
        <div class="page-title">
            {% block page_title %}Dashboard{% endblock %}
        </div>
        <div class="topbar-right">
            <span class="admin-name" style="color:var(--dark);">{{ request.user.username }}</span>
            <div class="avatar">{{ request.user.username|make_list|first|upper }}</div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
        {% block content %}{% endblock %}
    </main>
    
    <script>
        // Set active state on sidebar links
        const currentPath = window.location.pathname;
        const links = document.querySelectorAll('.nav-link');
        links.forEach(link => {
            if(link.getAttribute('href') !== '#' && currentPath.includes(link.getAttribute('href'))) {
                link.classList.add('active');
            }
        });
    </script>
    {% block scripts %}{% endblock %}
</body>
</html>
"""

files_to_write["templates/dashboard/home.html"] = """{% extends 'dashboard/base_dashboard.html' %}

{% block page_title %}Dashboard Overview{% endblock %}

{% block content %}
<div class="stats-grid">
    <div class="stat-card c-vehicles">
        <span class="stat-label">Total Vehicles</span>
        <h2 class="stat-number">{{ total_vehicles }}</h2>
        <div style="font-size:3rem; position:absolute; right:20px; bottom:20px; opacity:0.1;">🚗</div>
    </div>
    <div class="stat-card c-equipment">
        <span class="stat-label">Total Equipment</span>
        <h2 class="stat-number">{{ total_equipment }}</h2>
        <div style="font-size:3rem; position:absolute; right:20px; bottom:20px; opacity:0.1;">🎒</div>
    </div>
    <div class="stat-card c-bookings">
        <span class="stat-label">Bookings Today</span>
        <h2 class="stat-number">{{ total_bookings }}</h2>
        <div style="font-size:3rem; position:absolute; right:20px; bottom:20px; opacity:0.1;">📅</div>
    </div>
    <div class="stat-card c-users">
        <span class="stat-label">Total Users</span>
        <h2 class="stat-number">{{ total_users }}</h2>
        <div style="font-size:3rem; position:absolute; right:20px; bottom:20px; opacity:0.1;">👥</div>
    </div>
</div>

<div class="table-section">
    <h3 class="section-title">Recent Bookings</h3>
    <table class="data-table">
        <thead>
            <tr>
                <th>Booking ID</th>
                <th>User</th>
                <th>Item</th>
                <th>Dates</th>
                <th>Total Price</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {% for b in recent_bookings %}
            <tr>
                <td>#{{ b.id }}</td>
                <td>{{ b.user.username }}</td>
                <td>{% if b.vehicle %}{{ b.vehicle.name }}{% else %}-{% endif %}</td>
                <td>{{ b.start_date|date:"M d" }} - {{ b.end_date|date:"M d" }}</td>
                <td>${{ b.total_price }}</td>
                <td>
                    <span class="badge {{ b.status }}">{{ b.status|title }}</span>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="6" style="text-align:center; padding: 24px;">No recent bookings</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
"""

files_to_write["templates/dashboard/vehicles/list.html"] = """{% extends 'dashboard/base_dashboard.html' %}
{% load static %}

{% block page_title %}Vehicles{% endblock %}

{% block content %}
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:24px;">
    <h2 class="section-title" style="margin:0;">Manage Vehicles</h2>
    <a href="{% url 'vehicle_add' %}" class="btn btn-primary">Add Vehicle</a>
</div>

<div class="table-section">
    <table class="data-table">
        <thead>
            <tr>
                <th>Image</th>
                <th>Name</th>
                <th>Type</th>
                <th>Price/day</th>
                <th>Available</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for vehicle in vehicles %}
            <tr>
                <td>
                    {% if vehicle.image %}
                    <img src="{{ vehicle.image.url }}" alt="{{ vehicle.name }}" style="width:50px; height:50px; object-fit:cover; border-radius:4px;">
                    {% else %}
                    <div style="width:50px; height:50px; background:#eee; border-radius:4px;"></div>
                    {% endif %}
                </td>
                <td>{{ vehicle.name }}</td>
                <td style="text-transform:capitalize;">{{ vehicle.type }}</td>
                <td>${{ vehicle.price_per_day }}</td>
                <td>
                    <span class="status-dot {% if vehicle.is_available %}available{% else %}unavailable{% endif %}">●</span>
                </td>
                <td>
                    <a href="{% url 'vehicle_edit' vehicle.pk %}" class="btn btn-small btn-outline-forest">Edit</a>
                    <button class="btn btn-small btn-outline-danger" onclick="openDeleteModal('{% url 'vehicle_delete' vehicle.pk %}')">Delete</button>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="6" style="text-align:center; padding: 24px;">No vehicles found</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

<!-- Modal -->
<div class="modal-overlay" id="deleteModal">
    <div class="modal-box">
        <h3>Are you sure?</h3>
        <p style="color:var(--mist); margin-bottom:24px;">This action cannot be undone.</p>
        <form method="POST" id="deleteForm" style="display:inline-block;">
            {% csrf_token %}
            <button type="button" class="btn btn-text" onclick="closeDeleteModal()" style="margin-right:12px;">Cancel</button>
            <button type="submit" class="btn btn-primary" style="background:var(--danger)">Delete</button>
        </form>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script>
    function openDeleteModal(url) {
        document.getElementById('deleteForm').action = url;
        document.getElementById('deleteModal').classList.add('active');
    }
    function closeDeleteModal() {
        document.getElementById('deleteModal').classList.remove('active');
    }
</script>
{% endblock %}
"""

files_to_write["templates/dashboard/vehicles/form.html"] = """{% extends 'dashboard/base_dashboard.html' %}

{% block page_title %}{{ title }}{% endblock %}

{% block content %}
<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    <div class="form-grid">
        <div class="form-left-col">
            <div class="form-group">
                <label>Name</label>
                {{ form.name }}
                {{ form.name.errors }}
            </div>
            <div class="form-group">
                <label>Type</label>
                {{ form.type }}
                {{ form.type.errors }}
            </div>
            <div class="form-group">
                <label>Description</label>
                {{ form.description }}
                {{ form.description.errors }}
            </div>
            <div class="form-group">
                <label>Price Per Day ($)</label>
                {{ form.price_per_day }}
                {{ form.price_per_day.errors }}
            </div>
            <div class="form-group" style="display:flex; align-items:center; gap:12px;">
                <label style="margin:0;">Available</label>
                <div class="toggle-switch">
                    {{ form.is_available }}
                </div>
            </div>
        </div>
        
        <div class="form-right-col">
            <div class="form-group">
                <label>Image Upload</label>
                <label for="{{ form.image.id_for_label }}" class="image-upload-area" id="drop-area">
                    <span>Click or drag image to upload</span>
                    <img id="image-preview" class="image-preview" {% if object and object.image %}src="{{ object.image.url }}" style="display:block;"{% endif %}>
                </label>
                <div style="display:none;">
                    {{ form.image }}
                </div>
                {{ form.image.errors }}
            </div>
        </div>
    </div>
    
    <div style="margin-top:24px; text-align:right;">
        <a href="{% url 'vehicle_list' %}" class="btn btn-text" style="margin-right:16px;">Cancel</a>
        <button type="submit" class="btn btn-primary" style="padding: 12px 32px;">Save Vehicle</button>
    </div>
</form>
{% endblock %}

{% block scripts %}
<script>
    // Style inputs
    document.querySelectorAll('input[type="text"], input[type="number"], select, textarea').forEach(el => {
        el.classList.add('form-control');
    });

    // Toggle switch logic
    const checkbox = document.querySelector('input[name="is_available"]');
    if(checkbox) {
        let switchLabel = document.createElement('label');
        switchLabel.setAttribute('for', checkbox.id);
        checkbox.parentNode.insertBefore(switchLabel, checkbox.nextSibling);
    }

    // Image preview
    const fileInput = document.querySelector('input[type="file"]');
    const preview = document.getElementById('image-preview');
    if(fileInput) {
        fileInput.addEventListener('change', function() {
            const file = this.files[0];
            if(file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                }
                reader.readAsDataURL(file);
            }
        });
    }
</script>
{% endblock %}
"""

import os
for rel_path, content in files_to_write.items():
    full_path = os.path.join(BASE_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\\n")
    print(f"Wrote {full_path}")
