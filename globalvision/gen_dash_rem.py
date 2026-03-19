import os

TEMPLATES_DIR = r'c:\Users\Acer\Desktop\GlobalVision\globalvision\templates'

blog_list = """{% extends 'dashboard/base_dashboard.html' %}
{% block page_title %}Blog Posts{% endblock %}

{% block content %}
<div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
    <h2 style="font-family: var(--font-display); color: var(--dark);">Blog Posts</h2>
    <a href="{% url 'blog_add' %}" class="btn-primary">Write Post</a>
</div>

<table class="table">
    <thead>
        <tr>
            <th>Cover Image</th>
            <th>Title</th>
            <th>Status</th>
            <th>Date</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for obj in posts %}
        <tr>
            <td>
                {% if obj.cover_image %}
                <img src="{{ obj.cover_image.url }}" alt="{{ obj.title }}" style="width: 80px; height: 50px; object-fit: cover; border-radius: 4px;">
                {% endif %}
            </td>
            <td style="font-weight: 600; font-family: var(--font-display);">{{ obj.title }}</td>
            <td>
                {% if obj.status == 'published' %}
                <span class="pill pill-success">Published</span>
                {% else %}
                <span class="pill pill-warning">Draft</span>
                {% endif %}
            </td>
            <td>{% if obj.published_at %}{{ obj.published_at|date:"M d, Y" }}{% else %}-{% endif %}</td>
            <td>
                <a href="{% url 'blog_edit' obj.id %}" class="btn-outline" style="margin-right: 8px;">Edit</a>
                <button type="button" class="btn-outline-danger" onclick="openDeleteModal('{% url 'blog_delete' obj.id %}')">Delete</button>
            </td>
        </tr>
        {% empty %}
        <tr><td colspan="5" style="text-align:center; color: var(--mist);">No blog posts found.</td></tr>
        {% endfor %}
    </tbody>
</table>

<div class="modal-overlay" id="deleteModal">
    <div class="modal-box">
        <h3>Are you sure?</h3>
        <p>This action cannot be undone. Are you absolutely certain you want to delete this post?</p>
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

blog_form = """{% extends 'dashboard/base_dashboard.html' %}
{% block page_title %}{{ title }}{% endblock %}

{% block extra_css %}
.blog-form-container {
    background: white;
    padding: 30px;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
}

.title-input {
    font-size: 1.4rem;
    border: none;
    border-bottom: 2px solid var(--border);
    border-radius: 0;
    padding: 8px 0;
    width: 100%;
    margin-bottom: 30px;
    font-family: var(--font-display);
    font-weight: 600;
    color: var(--dark);
    outline: none;
    transition: var(--transition);
}

.title-input:focus {
    border-bottom-color: var(--forest);
}

.summernote-wrapper {
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    margin-bottom: 30px;
}

.image-upload-area {
    border: 2px dashed var(--border);
    border-radius: var(--radius);
    padding: 30px;
    text-align: center;
    color: var(--mist);
    cursor: pointer;
    transition: var(--transition);
    position: relative;
    height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 30px;
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

.status-toggle {
    display: flex;
    margin-bottom: 30px;
}

.status-toggle input { display: none; }
.status-label {
    padding: 10px 24px;
    border: 1px solid var(--border);
    background: white;
    color: var(--dark);
    cursor: pointer;
    font-weight: 500;
    font-size: 0.9rem;
    transition: var(--transition);
}

.status-label:first-of-type { border-radius: var(--radius) 0 0 var(--radius); border-right: none; }
.status-label:last-of-type { border-radius: 0 var(--radius) var(--radius) 0; }

.status-toggle input:checked + .status-label {
    background: var(--forest);
    color: white;
    border-color: var(--forest);
}

.buttons-row {
    display: flex;
    justify-content: flex-end;
    gap: 20px;
    align-items: center;
}
{% endblock %}

{% block content %}
<form method="POST" enctype="multipart/form-data" class="blog-form-container">
    {% csrf_token %}
    
    {{ form.title.errors }}
    <input type="text" name="title" class="title-input" placeholder="Post Title" value="{{ form.title.value|default:'' }}" required>
    
    <label style="font-size: 0.8rem; text-transform:uppercase; color: var(--mist); font-weight: 600; margin-bottom: 8px; display:block;">Cover Image</label>
    <label class="image-upload-area" id="uploadArea">
        <i class="fa-solid fa-image" style="font-size: 24px; margin-bottom: 10px;"></i>
        <span style="font-size: 13px;">Upload Cover Image</span>
        <input type="file" name="cover_image" style="display:none;" id="fileInput">
        <img id="imgPreview" class="image-preview" {% if object.cover_image %}src="{{ object.cover_image.url }}" style="display:block;"{% endif %}>
    </label>
    
    <div class="summernote-wrapper">
        {{ form.content }}
    </div>
    
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div class="status-toggle">
            <input type="radio" id="status_draft" name="status" value="draft" {% if form.status.value == 'draft' or not form.status.value %}checked{% endif %}>
            <label for="status_draft" class="status-label">Draft</label>
            
            <input type="radio" id="status_pub" name="status" value="published" {% if form.status.value == 'published' %}checked{% endif %}>
            <label for="status_pub" class="status-label">Published</label>
        </div>
        
        <div class="buttons-row">
            <a href="{% url 'blog_list' %}" style="color: var(--mist); text-decoration: none; font-weight: 500;">Cancel</a>
            <button type="submit" class="btn-primary" style="padding: 12px 32px;">Save Post</button>
        </div>
    </div>
</form>
{% endblock %}

{% block extra_scripts %}
<script>
    const fileInput = document.getElementById('fileInput');
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


about_editor = """{% extends 'dashboard/base_dashboard.html' %}
{% block page_title %}About Us Editor{% endblock %}

{% block extra_css %}
.card {
    background: white;
    padding: 28px;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    margin-bottom: 30px;
}
.card h3 {
    font-family: var(--font-display);
    margin-bottom: 20px;
    color: var(--dark);
}
.form-group { margin-bottom: 20px; }
.form-label {
    font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1.5px;
    color: var(--dark); display: block; margin-bottom: 8px; font-weight: 700;
}
.form-control {
    width: 100%; padding: 12px 16px; border: 1px solid var(--border);
    border-radius: var(--radius); font-family: var(--font-body); font-size: 0.95rem;
    outline: none; transition: var(--transition);
}
.form-control:focus { border-color: var(--forest); }
.stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.stats-grid .form-control { text-align: center; font-size: 1.2rem; font-weight: 700; }

.member-card {
    display: grid; grid-template-columns: 120px 1fr; gap: 20px;
    padding: 20px; border: 1px solid var(--border); border-radius: var(--radius);
    margin-bottom: 15px; position: relative;
}
.btn-remove-member {
    position: absolute; top: 15px; right: 15px;
    color: var(--danger); background: none; border: none; cursor: pointer;
    font-size: 16px;
}
.img-upload {
    width: 120px; height: 120px; border: 2px dashed var(--border);
    border-radius: var(--radius); display: flex; align-items: center;
    justify-content: center; color: var(--mist); cursor: pointer;
    position: relative; overflow: hidden;
}
.img-upload img { width: 100%; height: 100%; object-fit: cover; position: absolute; }
.img-upload input { display: none; }
.btn-add-member {
    width: 100%; border: 2px dashed var(--forest); color: var(--forest);
    background: transparent; padding: 14px; border-radius: var(--radius);
    cursor: pointer; font-weight: 600; text-align: center;
    transition: var(--transition);
}
.btn-add-member:hover { background: rgba(45,74,53,0.05); }
{% endblock %}

{% block content %}
<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    
    <div class="card">
        <h3>Hero Content</h3>
        <div class="form-group">
            <label class="form-label">Tagline</label>
            <input type="text" name="tagline" class="form-control" value="{{ about.tagline }}">
        </div>
        <div class="form-group">
            <label class="form-label">Company Story</label>
            <textarea name="company_story" class="form-control" style="min-height:100px;">{{ about.company_story }}</textarea>
        </div>
        <div class="form-group">
            <label class="form-label">Mission Statement</label>
            <textarea name="mission_statement" class="form-control" style="min-height:80px;">{{ about.mission_statement }}</textarea>
        </div>
    </div>
    
    <div class="card">
        <h3>Stats</h3>
        <div class="stats-grid">
            <div class="form-group">
                <label class="form-label" style="text-align:center;">Happy Trekkers</label>
                <input type="number" name="stat_trekkers" class="form-control" value="{{ about.stat_trekkers }}">
            </div>
            <div class="form-group">
                <label class="form-label" style="text-align:center;">Total Vehicles</label>
                <input type="number" name="stat_vehicles" class="form-control" value="{{ about.stat_vehicles }}">
            </div>
            <div class="form-group">
                <label class="form-label" style="text-align:center;">Equipment Items</label>
                <input type="number" name="stat_equipment" class="form-control" value="{{ about.stat_equipment }}">
            </div>
        </div>
    </div>
    
    <div class="card">
        <h3>Team Members</h3>
        <input type="hidden" name="deleted_members" id="deleted_members" value="">
        <div id="members-container">
            {% for member in team_members %}
            <div class="member-card" id="member_{{ member.id }}">
                <button type="button" class="btn-remove-member" onclick="removeMember({{ member.id }})"><i class="fa-solid fa-xmark"></i></button>
                <label class="img-upload">
                    <i class="fa-solid fa-camera"></i>
                    <input type="file" name="member_photo_{{ member.id }}" onchange="previewImg(this)">
                    {% if member.photo %}
                    <img src="{{ member.photo.url }}">
                    {% else %}
                    <img>
                    {% endif %}
                </label>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                    <input type="text" name="member_name_{{ member.id }}" class="form-control" value="{{ member.name }}" placeholder="Name">
                    <input type="text" name="member_role_{{ member.id }}" class="form-control" value="{{ member.role }}" placeholder="Role">
                    <input type="text" name="member_bio_{{ member.id }}" class="form-control" value="{{ member.bio }}" placeholder="Short Bio" style="grid-column: 1 / -1;">
                    <input type="text" name="member_fav_{{ member.id }}" class="form-control" value="{{ member.favorite_trek }}" placeholder="Favorite Trek" style="grid-column: 1 / -1;">
                </div>
            </div>
            {% endfor %}
        </div>
        <button type="button" class="btn-add-member" onclick="addMember()">+ Add Team Member</button>
    </div>
    
    <div style="margin-bottom: 50px;">
        <button type="submit" style="background: var(--gold); color: var(--dark); font-size: 1rem; padding: 14px 40px; border-radius: var(--radius); font-weight: 600; border: none; float: right; cursor:pointer;">Save All</button>
    </div>
</form>
{% endblock %}

{% block extra_scripts %}
<script>
    let newMemberCounter = 0;
    
    function previewImg(input) {
        if(input.files && input.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                let img = input.parentElement.querySelector('img');
                if(!img) {
                    img = document.createElement('img');
                    input.parentElement.appendChild(img);
                }
                img.src = e.target.result;
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    function removeMember(id, isNew) {
        if(!isNew) {
            const delInput = document.getElementById('deleted_members');
            delInput.value += id + ',';
            document.getElementById('member_' + id).style.display = 'none';
        } else {
            document.getElementById('new_member_' + id).remove();
        }
    }

    function addMember() {
        newMemberCounter++;
        const id = 'new' + newMemberCounter;
        const card = document.createElement('div');
        card.className = 'member-card';
        card.id = 'new_member_' + newMemberCounter;
        card.innerHTML = `
            <button type="button" class="btn-remove-member" onclick="removeMember(${newMemberCounter}, true)"><i class="fa-solid fa-xmark"></i></button>
            <label class="img-upload">
                <i class="fa-solid fa-camera"></i>
                <input type="file" name="member_photo_${id}" onchange="previewImg(this)">
            </label>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <input type="text" name="member_name_${id}" class="form-control" placeholder="Name" required>
                <input type="text" name="member_role_${id}" class="form-control" placeholder="Role" required>
                <input type="text" name="member_bio_${id}" class="form-control" placeholder="Short Bio" style="grid-column: 1 / -1;" required>
                <input type="text" name="member_fav_${id}" class="form-control" placeholder="Favorite Trek" style="grid-column: 1 / -1;" required>
            </div>
        `;
        document.getElementById('members-container').appendChild(card);
    }
</script>
{% endblock %}
"""


contact_editor = """{% extends 'dashboard/base_dashboard.html' %}
{% block page_title %}Contact Us Editor{% endblock %}

{% block extra_css %}
.contact-grid {
    display: grid;
    grid-template-columns: 60% 40%;
    gap: 30px;
}
.card {
    background: white; padding: 30px; border-radius: var(--radius); box-shadow: var(--shadow);
}
.form-group { margin-bottom: 20px; }
.form-label {
    font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1.5px;
    color: var(--dark); display: block; margin-bottom: 8px; font-weight: 700;
}
.form-control {
    width: 100%; padding: 12px 16px; border: 1px solid var(--border);
    border-radius: var(--radius); font-family: var(--font-body); font-size: 0.95rem;
    outline: none; transition: var(--transition);
}
.form-control:focus { border-color: var(--forest); }
.iframe-preview {
    width: 100%; height: 300px; border: 1px solid var(--border); border-radius: var(--radius); margin-top: 20px;
}
{% endblock %}

{% block content %}
<form method="POST">
    {% csrf_token %}
    <div class="contact-grid">
        <div class="card">
            <h3 style="font-family: var(--font-display); margin-bottom: 20px;">Contact Details</h3>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div class="form-group">
                    <label class="form-label">Phone</label>
                    <input type="text" name="phone" class="form-control" value="{{ settings.phone }}">
                </div>
                <div class="form-group">
                    <label class="form-label">Email</label>
                    <input type="email" name="email" class="form-control" value="{{ settings.email }}">
                </div>
            </div>
            
            <div class="form-group">
                <label class="form-label">WhatsApp</label>
                <input type="text" name="whatsapp" class="form-control" value="{{ settings.whatsapp }}">
            </div>
            
            <div class="form-group">
                <label class="form-label">Physical Address</label>
                <textarea name="address" class="form-control" style="min-height: 80px;">{{ settings.address }}</textarea>
            </div>
            
            <div class="form-group">
                <label class="form-label">Opening Hours</label>
                <textarea name="opening_hours" class="form-control" style="min-height: 80px;">{{ settings.opening_hours }}</textarea>
            </div>
            
            <button type="submit" class="btn-primary" style="width:100%; font-size: 1rem; padding: 14px;">Save Contact Details</button>
        </div>
        
        <div class="card">
            <h3 style="font-family: var(--font-display); margin-bottom: 20px;">Google Maps Embed</h3>
            <div class="form-group">
                <label class="form-label">Maps Embed URL (src only)</label>
                <input type="text" name="maps_embed" id="maps-input" class="form-control" value="{{ settings.maps_embed }}">
            </div>
            <label class="form-label">Preview</label>
            <iframe id="maps-preview" class="iframe-preview" src="{{ settings.maps_embed }}"></iframe>
        </div>
    </div>
</form>
{% endblock %}

{% block extra_scripts %}
<script>
    document.getElementById('maps-input').addEventListener('input', function() {
        document.getElementById('maps-preview').src = this.value;
    });
</script>
{% endblock %}
"""


os.makedirs(os.path.join(TEMPLATES_DIR, 'dashboard', 'blog'), exist_ok=True)
with open(os.path.join(TEMPLATES_DIR, 'dashboard', 'blog', 'list.html'), 'w', encoding='utf-8') as f: f.write(blog_list)
with open(os.path.join(TEMPLATES_DIR, 'dashboard', 'blog', 'form.html'), 'w', encoding='utf-8') as f: f.write(blog_form)

with open(os.path.join(TEMPLATES_DIR, 'dashboard', 'about.html'), 'w', encoding='utf-8') as f: f.write(about_editor)
with open(os.path.join(TEMPLATES_DIR, 'dashboard', 'contact.html'), 'w', encoding='utf-8') as f: f.write(contact_editor)
