import os

TEMPLATES_DIR = r'c:\Users\Acer\Desktop\GlobalVision\globalvision\templates'

auth_login = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Admin Portal | PeakRent</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
<style>
:root {
  --cream: #F5F0E8;
  --dark: #1A1A14;
  --forest: #2D4A35;
  --moss: #4E7A57;
  --gold: #C8933A;
  --warm: #E8DCC8;
  --mist: #8BA89A;
  --sidebar-bg: #141F17;
  --sidebar-text: rgba(245,240,232,0.6);
  --sidebar-active: #C8933A;
  --card-bg: #FFFFFF;
  --border: rgba(26,26,20,0.1);
  --danger: #C0392B;
  --success: #27AE60;
  --font-display: 'Playfair Display', serif;
  --font-body: 'DM Sans', sans-serif;
  --radius: 6px;
  --shadow: 0 2px 12px rgba(0,0,0,0.08);
  --transition: all 0.2s ease;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    background-color: var(--dark);
    font-family: var(--font-body);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
}

.login-card {
    background-color: var(--sidebar-bg);
    width: 420px;
    padding: 48px;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 8px;
}

.logo {
    text-align: center;
    font-family: var(--font-display);
    font-size: 32px;
    color: var(--gold);
    font-weight: 700;
    margin-bottom: 5px;
}

.logo span {
    color: white;
}

.subtitle {
    text-align: center;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--mist);
    margin-bottom: 30px;
}

.form-group {
    margin-bottom: 20px;
}

label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--mist);
    display: block;
    margin-bottom: 8px;
}

input {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    color: white;
    padding: 14px 16px;
    border-radius: var(--radius);
    width: 100%;
    font-family: var(--font-body);
    font-size: 15px;
    transition: var(--transition);
}

input:focus {
    border-color: var(--gold);
    outline: none;
}

button {
    background: var(--gold);
    color: var(--dark);
    width: 100%;
    padding: 14px;
    font-weight: 600;
    border: none;
    border-radius: var(--radius);
    cursor: pointer;
    font-size: 15px;
    margin-top: 10px;
    transition: var(--transition);
}

button:hover {
    opacity: 0.9;
}

.error-pill {
    background: rgba(192, 57, 43, 0.15);
    color: #ff6b6b;
    border: 1px solid rgba(192, 57, 43, 0.3);
    padding: 10px 16px;
    border-radius: 20px;
    text-align: center;
    font-size: 13px;
    margin-bottom: 25px;
}
</style>
</head>
<body>
    <div class="login-card">
        <div class="logo"><span>Peak</span>Rent</div>
        <div class="subtitle">Admin Portal</div>
        
        {% if error %}
        <div class="error-pill">{{ error }}</div>
        {% endif %}
        
        <form method="POST">
            {% csrf_token %}
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" required>
            </div>
            <button type="submit">Sign In</button>
        </form>
    </div>
</body>
</html>
"""

base_dashboard = """{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{% block title %}Dashboard | PeakRent{% endblock %}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
:root {
  --cream: #F5F0E8;
  --dark: #1A1A14;
  --forest: #2D4A35;
  --moss: #4E7A57;
  --gold: #C8933A;
  --warm: #E8DCC8;
  --mist: #8BA89A;
  --sidebar-bg: #141F17;
  --sidebar-text: rgba(245,240,232,0.6);
  --sidebar-active: #C8933A;
  --card-bg: #FFFFFF;
  --border: rgba(26,26,20,0.1);
  --danger: #C0392B;
  --success: #27AE60;
  --font-display: 'Playfair Display', serif;
  --font-body: 'DM Sans', sans-serif;
  --radius: 6px;
  --shadow: 0 2px 12px rgba(0,0,0,0.08);
  --transition: all 0.2s ease;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    display: grid;
    grid-template-columns: 260px 1fr;
    grid-template-rows: 60px 1fr;
    min-height: 100vh;
    font-family: var(--font-body);
    background: #F8F6F1;
}

/* SIDEBAR */
.sidebar {
    grid-row: 1 / -1;
    background: var(--sidebar-bg);
    display: flex;
    flex-direction: column;
}

.brand {
    padding: 30px 20px;
    font-family: var(--font-display);
    font-size: 26px;
    font-weight: 700;
    color: white;
}

.brand span { color: var(--gold); }

.nav-section {
    font-size: 0.65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--mist);
    padding: 20px 20px 6px;
    font-weight: 700;
}

.nav-link {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 11px 20px;
    color: var(--sidebar-text);
    text-decoration: none;
    border-left: 3px solid transparent;
    transition: var(--transition);
    font-size: 0.9rem;
}

.nav-link:hover, .nav-link.active {
    color: white;
    border-left-color: var(--gold);
    background: rgba(200,147,58,0.08);
}

.sidebar-bottom {
    margin-top: auto;
    padding: 20px;
    border-top: 1px solid rgba(255,255,255,0.05);
    display: flex;
    align-items: center;
    gap: 12px;
}

.avatar {
    width: 36px;
    height: 36px;
    background: var(--forest);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
}

.admin-info {
    flex: 1;
}

.admin-name {
    color: white;
    font-size: 0.85rem;
    font-weight: 500;
}

.logout-link {
    color: var(--danger);
    font-size: 0.8rem;
    text-decoration: none;
}

/* TOPBAR */
.topbar {
    grid-column: 2;
    background: white;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 32px;
}

.page-title {
    font-family: var(--font-display);
    font-size: 20px;
    font-weight: 600;
    color: var(--dark);
}

/* MAIN CONTENT */
.main-content {
    grid-column: 2;
    grid-row: 2;
    padding: 32px;
    overflow-y: auto;
}

/* GLOBAL ADMIN STYLES */
.btn-primary {
    background: var(--forest);
    color: white;
    padding: 10px 24px;
    border-radius: var(--radius);
    text-decoration: none;
    font-weight: 500;
    transition: var(--transition);
    border: none;
    cursor: pointer;
}

.btn-primary:hover {
    background: var(--moss);
}

.btn-outline {
    border: 1px solid var(--forest);
    color: var(--forest);
    padding: 6px 14px;
    border-radius: var(--radius);
    text-decoration: none;
    font-size: 13px;
    font-weight: 500;
    transition: var(--transition);
}

.btn-outline:hover {
    background: var(--forest);
    color: white;
}

.btn-outline-danger {
    border: 1px solid var(--danger);
    color: var(--danger);
    padding: 6px 14px;
    border-radius: var(--radius);
    text-decoration: none;
    font-size: 13px;
    font-weight: 500;
    transition: var(--transition);
    background: none;
    cursor: pointer;
}

.btn-outline-danger:hover {
    background: var(--danger);
    color: white;
}

.table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    box-shadow: var(--shadow);
    border-radius: var(--radius);
    overflow: hidden;
}

.table th {
    background: var(--forest);
    color: white;
    text-transform: uppercase;
    font-size: 0.78rem;
    padding: 14px 20px;
    text-align: left;
    letter-spacing: 1px;
}

.table td {
    padding: 16px 20px;
    border-bottom: 1px solid var(--border);
    font-size: 0.95rem;
    vertical-align: middle;
}

.table tr:hover {
    background: var(--cream);
}

.table tr:nth-child(even) {
    background: #FAFAF8;
}

/* Modal */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0,0,0,0.5);
    z-index: 1000;
    display: none;
    align-items: center;
    justify-content: center;
}

.modal-box {
    background: white;
    width: 400px;
    padding: 36px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}

.modal-box h3 { margin-bottom: 15px; font-family: var(--font-display); }
.modal-box p { margin-bottom: 25px; color: var(--mist); font-size: 15px; }

.modal-actions {
    display: flex;
    justify-content: center;
    gap: 15px;
}

.pill {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    display: inline-block;
}

.pill-success { background: #E8F5E9; color: #2E7D32; }
.pill-warning { background: #FFF8E1; color: #F57F17; }
.pill-danger { background: #FFEBEE; color: #C62828; }

{% block extra_css %}{% endblock %}
</style>
</head>
<body>

<div class="sidebar">
    <div class="brand">Peak<span>Rent</span></div>
    
    <div class="nav-section">Overview</div>
    <a href="{% url 'dashboard_home' %}" class="nav-link {% if request.resolver_match.url_name == 'dashboard_home' %}active{% endif %}"><i class="fa-solid fa-chart-pie"></i> Dashboard</a>
    
    <div class="nav-section">Content</div>
    <a href="{% url 'vehicle_list' %}" class="nav-link {% if 'vehicle' in request.resolver_match.url_name %}active{% endif %}"><i class="fa-solid fa-car"></i> Vehicles</a>
    <a href="{% url 'equipment_list' %}" class="nav-link {% if 'equipment' in request.resolver_match.url_name %}active{% endif %}"><i class="fa-solid fa-tent"></i> Equipment</a>
    <a href="#" class="nav-link"><i class="fa-solid fa-calendar-check"></i> Bookings</a>
    <a href="{% url 'blog_list' %}" class="nav-link {% if 'blog' in request.resolver_match.url_name %}active{% endif %}"><i class="fa-solid fa-pen-nib"></i> Blog Posts</a>
    
    <div class="nav-section">Pages</div>
    <a href="{% url 'about_editor' %}" class="nav-link {% if request.resolver_match.url_name == 'about_editor' %}active{% endif %}"><i class="fa-solid fa-address-card"></i> About Us</a>
    <a href="{% url 'contact_editor' %}" class="nav-link {% if request.resolver_match.url_name == 'contact_editor' %}active{% endif %}"><i class="fa-solid fa-envelope"></i> Contact Us</a>

    <div class="sidebar-bottom">
        <div class="avatar">{{ request.user.user_name|make_list|first|upper }}</div>
        <div class="admin-info">
            <div class="admin-name">{{ request.user.user_name }}</div>
            <a href="{% url 'admin_logout' %}" class="logout-link">Logout</a>
        </div>
    </div>
</div>

<div class="topbar">
    <div class="page-title">{% block page_title %}Dashboard{% endblock %}</div>
</div>

<div class="main-content">
    {% block content %}{% endblock %}
</div>

{% block extra_scripts %}{% endblock %}
</body>
</html>
"""

dashboard_home = """{% extends 'dashboard/base_dashboard.html' %}
{% block page_title %}Dashboard Overview{% endblock %}

{% block extra_css %}
.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
    margin-bottom: 40px;
}

.stat-card {
    background: white;
    padding: 28px;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    border-left: 4px solid var(--forest);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}

.stat-card:hover {
    transform: translateY(-2px);
}

.stat-card:nth-child(2) { border-left-color: var(--gold); }
.stat-card:nth-child(3) { border-left-color: var(--moss); }
.stat-card:nth-child(4) { border-left-color: var(--mist); }

.stat-label {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--mist);
    font-weight: 700;
    margin-bottom: 10px;
}

.stat-num {
    font-family: var(--font-display);
    font-size: 2.5rem;
    color: var(--dark);
    font-weight: 700;
}

.stat-icon {
    position: absolute;
    right: 20px;
    bottom: 20px;
    font-size: 48px;
    color: var(--dark);
    opacity: 0.05;
}

.section-title {
    font-family: var(--font-display);
    font-size: 22px;
    color: var(--dark);
    margin-bottom: 20px;
}
{% endblock %}

{% block content %}
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-label">Total Vehicles</div>
        <div class="stat-num">{{ total_vehicles }}</div>
        <i class="fa-solid fa-car stat-icon"></i>
    </div>
    <div class="stat-card">
        <div class="stat-label">Equipment Stock</div>
        <div class="stat-num">{{ total_equipment }}</div>
        <i class="fa-solid fa-tent stat-icon"></i>
    </div>
    <div class="stat-card">
        <div class="stat-label">Bookings Today</div>
        <div class="stat-num">{{ total_bookings }}</div>
        <i class="fa-solid fa-calendar-check stat-icon"></i>
    </div>
    <div class="stat-card">
        <div class="stat-label">Registered Users</div>
        <div class="stat-num">{{ total_users }}</div>
        <i class="fa-solid fa-users stat-icon"></i>
    </div>
</div>

<h2 class="section-title">Recent Bookings</h2>
<table class="table">
    <thead>
        <tr>
            <th>ID</th>
            <th>User</th>
            <th>Item</th>
            <th>Dates</th>
            <th>Amount</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
        {% for booking in recent_bookings %}
        <tr>
            <td>#{{ booking.id }}</td>
            <td>{{ booking.user.user_name }}</td>
            <td>{{ booking.vehicle.name }}</td>
            <td>{{ booking.start_date }} - {{ booking.end_date }}</td>
            <td>Rs. {{ booking.total_price }}</td>
            <td>
                {% if booking.status == 'confirmed' %}
                <span class="pill pill-success">Confirmed</span>
                {% elif booking.status == 'pending' %}
                <span class="pill pill-warning">Pending</span>
                {% else %}
                <span class="pill pill-danger">Cancelled</span>
                {% endif %}
            </td>
        </tr>
        {% empty %}
        <tr>
            <td colspan="6" style="text-align:center; color: var(--mist);">No recent bookings found.</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}
"""

os.makedirs(os.path.join(TEMPLATES_DIR, 'auth'), exist_ok=True)
with open(os.path.join(TEMPLATES_DIR, 'auth', 'admin_login.html'), 'w', encoding='utf-8') as f: f.write(auth_login)

os.makedirs(os.path.join(TEMPLATES_DIR, 'dashboard'), exist_ok=True)
with open(os.path.join(TEMPLATES_DIR, 'dashboard', 'base_dashboard.html'), 'w', encoding='utf-8') as f: f.write(base_dashboard)
with open(os.path.join(TEMPLATES_DIR, 'dashboard', 'home.html'), 'w', encoding='utf-8') as f: f.write(dashboard_home)
