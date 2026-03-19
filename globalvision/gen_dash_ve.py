import os

TEMPLATES_DIR = r'c:\Users\Acer\Desktop\GlobalVision\globalvision\templates'

vehicle_list = """{% extends 'dashboard/base_dashboard.html' %}
{% block page_title %}Vehicles{% endblock %}

{% block content %}
<div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
    <h2 style="font-family: var(--font-display); color: var(--dark);">Vehicles</h2>
    <a href="{% url 'vehicle_add' %}" class="btn-primary">Add Vehicle</a>
</div>

<table class="table">
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
        {% for obj in vehicles %}
        <tr>
            <td>
                {% if obj.image %}
                <img src="{{ obj.image.url }}" alt="{{ obj.name }}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;">
                {% endif %}
            </td>
            <td style="font-weight: 500;">{{ obj.name }}</td>
            <td style="text-transform: capitalize;">{{ obj.type }}</td>
            <td>Rs. {{ obj.price_per_day }}</td>
            <td>
                {% if obj.is_available %}
                <span style="color: var(--success); font-size: 1.2rem;">●</span>
                {% else %}
                <span style="color: var(--danger); font-size: 1.2rem;">●</span>
                {% endif %}
            </td>
            <td>
                <a href="{% url 'vehicle_edit' obj.id %}" class="btn-outline" style="margin-right: 8px;">Edit</a>
                <button type="button" class="btn-outline-danger" onclick="openDeleteModal('{% url 'vehicle_delete' obj.id %}')">Delete</button>
            </td>
        </tr>
        {% empty %}
        <tr><td colspan="6" style="text-align:center; color: var(--mist);">No vehicles found.</td></tr>
        {% endfor %}
    </tbody>
</table>

<!-- Delete Modal using pure CSS/JS -->
<div class="modal-overlay" id="deleteModal">
    <div class="modal-box">
        <h3>Are you sure?</h3>
        <p>This action cannot be undone. Are you absolutely certain you want to delete this vehicle?</p>
        <div class="modal-actions">
            <button type="button" class="btn-outline" onclick="closeDeleteModal()">Cancel</button>
            <form id="deleteForm" method="POST" style="display:inline;">
                {% csrf_token %}
                <button type="submit" class="btn-primary" style="background: var(--danger);">Delete</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_scripts %}
<script>
    function openDeleteModal(url) {
        document.getElementById('deleteForm').action = url;
        document.getElementById('deleteModal').style.display = 'flex';
    }
    function closeDeleteModal() {
        document.getElementById('deleteModal').style.display = 'none';
        document.getElementById('deleteForm').action = '';
    }
</script>
{% endblock %}
"""

vehicle_form = """{% extends 'dashboard/base_dashboard.html' %}
{% block page_title %}{{ title }}{% endblock %}

{% block extra_css %}
.form-grid {
    display: grid;
    grid-template-columns: 60% 40%;
    gap: 30px;
    background: white;
    padding: 30px;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
}

.form-group {
    margin-bottom: 20px;
}

.form-label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: var(--dark);
    display: block;
    margin-bottom: 8px;
    font-weight: 700;
}

.form-control {
    width: 100%;
    padding: 12px 16px;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    font-family: var(--font-body);
    font-size: 0.95rem;
    outline: none;
    transition: var(--transition);
}

.form-control:focus {
    border-color: var(--forest);
    box-shadow: 0 0 0 3px rgba(45,74,53,0.1);
}

textarea.form-control {
    min-height: 120px;
    resize: vertical;
}

select.form-control {
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath fill='%231A1A14' d='M1 4l5 5 5-5z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 16px center;
}

.toggle-switch {
    display: flex;
    align-items: center;
    cursor: pointer;
}

.toggle-switch input { display: none; }

.toggle-slider {
    width: 44px;
    height: 24px;
    background: var(--mist);
    border-radius: 20px;
    position: relative;
    transition: var(--transition);
    margin-right: 12px;
}

.toggle-slider::after {
    content: '';
    position: absolute;
    width: 18px;
    height: 18px;
    background: white;
    border-radius: 50%;
    top: 3px;
    left: 3px;
    transition: var(--transition);
}

.toggle-switch input:checked + .toggle-slider { background: var(--forest); }
.toggle-switch input:checked + .toggle-slider::after { transform: translateX(20px); }

.image-upload-area {
    border: 2px dashed var(--border);
    border-radius: var(--radius);
    padding: 40px 20px;
    text-align: center;
    color: var(--mist);
    cursor: pointer;
    transition: var(--transition);
    position: relative;
    height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
}

.image-upload-area:hover { border-color: var(--forest); }

.image-preview {
    width: 100%;
    height: 100%;
    object-fit: cover;
    position: absolute;
    top: 0;
    left: 0;
    border-radius: var(--radius);
    display: none;
}

.buttons-row {
    margin-top: 30px;
    display: flex;
    justify-content: flex-end;
    gap: 20px;
    align-items: center;
}

.btn-cancel {
    color: var(--mist);
    text-decoration: none;
    font-weight: 500;
}

.btn-cancel:hover { color: var(--dark); }
{% endblock %}

{% block content %}
<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    <div class="form-grid">
        <div class="left-col">
            <h2 style="font-family: var(--font-display); margin-bottom: 25px;">{{ title }}</h2>
            
            <div class="form-group">
                <label class="form-label">Name</label>
                {{ form.name }}
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div class="form-group">
                    <label class="form-label">Type</label>
                    {{ form.type }}
                </div>
                <div class="form-group">
                    <label class="form-label">Price per Day (Rs)</label>
                    {{ form.price_per_day }}
                </div>
            </div>
            
            <div class="form-group">
                <label class="form-label">Description</label>
                {{ form.description }}
            </div>
            
            <div class="form-group">
                <label class="form-label">Availability</label>
                <label class="toggle-switch">
                    {{ form.is_available }}
                    <div class="toggle-slider"></div>
                    <span style="font-size: 14px; color: var(--dark); font-weight: 600;">Currently Available</span>
                </label>
            </div>
        </div>
        
        <div class="right-col">
            <label class="form-label">Vehicle Image</label>
            <label class="image-upload-area" id="uploadArea">
                <i class="fa-solid fa-cloud-arrow-up" style="font-size: 32px; margin-bottom: 15px;"></i>
                <span style="font-size: 14px; font-weight: 500;">Click to upload image</span>
                {{ form.image }}
                <img id="imgPreview" class="image-preview" {% if object.image %}src="{{ object.image.url }}" style="display:block;"{% endif %}>
            </label>
        </div>
    </div>
    
    <div class="buttons-row">
        <a href="{% url 'vehicle_list' %}" class="btn-cancel">Cancel</a>
        <button type="submit" class="btn-primary" style="padding: 12px 32px;">Save Vehicle</button>
    </div>
</form>
{% endblock %}

{% block extra_scripts %}
<script>
    // Style django generated fields
    document.querySelectorAll('input[type=text], input[type=number], select, textarea').forEach(el => {
        el.classList.add('form-control');
    });
    
    // Hide standard clear checkbox from image field
    document.querySelectorAll('input[type=checkbox]:not([name=is_available])').forEach(el => {
        el.style.display = 'none';
    });
    
    const fileInput = document.querySelector('input[type=file]');
    fileInput.style.display = 'none';
    fileInput.addEventListener('change', function(e) {
        if(e.target.files && e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                document.getElementById('imgPreview').src = e.target.result;
                document.getElementById('imgPreview').style.display = 'block';
            }
            reader.readAsDataURL(e.target.files[0]);
        }
    });
</script>
{% endblock %}
"""


equipment_list = vehicle_list.replace('Vehicle', 'Equipment').replace('vehicle', 'equipment').replace('{{ obj.type }}', '{{ obj.category }}').replace('Type', 'Category').replace('Available', 'Stock').replace('{% if obj.is_available %}', '').replace('<span style="color: var(--success); font-size: 1.2rem;">●</span>', '<span style="background: rgba(45,74,53,0.1); color: var(--forest); padding: 4px 10px; border-radius: 20px; font-weight: 500;">{{ obj.stock }} In Stock</span>').replace('{% else %}', '').replace('<span style="color: var(--danger); font-size: 1.2rem;">●</span>', '').replace('{% endif %}', '')

equipment_form = vehicle_form.replace('Vehicle', 'Equipment').replace('vehicle', 'equipment').replace('type', 'category').replace('Type', 'Category').replace('{{ form.is_available }}', '{{ form.stock }}').replace('<div class="toggle-slider"></div>', '').replace('<span style="font-size: 14px; color: var(--dark); font-weight: 600;">Currently Available</span>', '').replace('<label class="toggle-switch">', '').replace('</label>', '').replace('Availability', 'Stock')

os.makedirs(os.path.join(TEMPLATES_DIR, 'dashboard', 'vehicles'), exist_ok=True)
with open(os.path.join(TEMPLATES_DIR, 'dashboard', 'vehicles', 'list.html'), 'w', encoding='utf-8') as f: f.write(vehicle_list)
with open(os.path.join(TEMPLATES_DIR, 'dashboard', 'vehicles', 'form.html'), 'w', encoding='utf-8') as f: f.write(vehicle_form)

os.makedirs(os.path.join(TEMPLATES_DIR, 'dashboard', 'equipment'), exist_ok=True)
with open(os.path.join(TEMPLATES_DIR, 'dashboard', 'equipment', 'list.html'), 'w', encoding='utf-8') as f: f.write(equipment_list)
with open(os.path.join(TEMPLATES_DIR, 'dashboard', 'equipment', 'form.html'), 'w', encoding='utf-8') as f: f.write(equipment_form)

