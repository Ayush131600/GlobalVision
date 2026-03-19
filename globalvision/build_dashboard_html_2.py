import os

BASE_DIR = r"c:\Users\Acer\Desktop\GlobalVision\globalvision"

files_to_write = {}

files_to_write["templates/dashboard/equipment/list.html"] = """{% extends 'dashboard/base_dashboard.html' %}
{% load static %}

{% block page_title %}Equipment{% endblock %}

{% block content %}
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:24px;">
    <h2 class="section-title" style="margin:0;">Manage Equipment</h2>
    <a href="{% url 'equipment_add' %}" class="btn btn-primary">Add Equipment</a>
</div>

<div class="table-section">
    <table class="data-table">
        <thead>
            <tr>
                <th>Image</th>
                <th>Name</th>
                <th>Category</th>
                <th>Price/day</th>
                <th>Stock</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for item in equipment %}
            <tr>
                <td>
                    {% if item.image %}
                    <img src="{{ item.image.url }}" alt="{{ item.name }}" style="width:50px; height:50px; object-fit:cover; border-radius:4px;">
                    {% else %}
                    <div style="width:50px; height:50px; background:#eee; border-radius:4px;"></div>
                    {% endif %}
                </td>
                <td>{{ item.name }}</td>
                <td style="text-transform:capitalize;">{{ item.category }}</td>
                <td>${{ item.price_per_day }}</td>
                <td>
                    <span class="stock-badge">{{ item.stock }}</span>
                </td>
                <td>
                    <a href="{% url 'equipment_edit' item.pk %}" class="btn btn-small btn-outline-forest">Edit</a>
                    <form method="POST" action="{% url 'equipment_delete' item.pk %}" style="display:inline-block;" onsubmit="return confirm('Are you sure you want to delete this item?');">
                        {% csrf_token %}
                        <button type="submit" class="btn btn-small btn-outline-danger">Delete</button>
                    </form>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="6" style="text-align:center; padding: 24px;">No equipment found</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
"""

files_to_write["templates/dashboard/equipment/form.html"] = """{% extends 'dashboard/base_dashboard.html' %}

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
                <label>Category</label>
                {{ form.category }}
                {{ form.category.errors }}
            </div>
            <div class="form-group">
                <label>Description</label>
                {{ form.description }}
                {{ form.description.errors }}
            </div>
            <div class="form-group" style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
                <div>
                    <label>Price Per Day ($)</label>
                    {{ form.price_per_day }}
                    {{ form.price_per_day.errors }}
                </div>
                <div>
                    <label>Stock</label>
                    {{ form.stock }}
                    {{ form.stock.errors }}
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
        <a href="{% url 'equipment_list' %}" class="btn btn-text" style="margin-right:16px;">Cancel</a>
        <button type="submit" class="btn btn-primary" style="padding: 12px 32px;">Save Equipment</button>
    </div>
</form>
{% endblock %}

{% block scripts %}
<script>
    document.querySelectorAll('input[type="text"], input[type="number"], select, textarea').forEach(el => {
        el.classList.add('form-control');
    });

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

files_to_write["templates/dashboard/blog/list.html"] = """{% extends 'dashboard/base_dashboard.html' %}
{% load static %}

{% block page_title %}Blog Posts{% endblock %}

{% block content %}
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:24px;">
    <h2 class="section-title" style="margin:0;">Manage Blog Posts</h2>
    <a href="{% url 'blog_add' %}" class="btn btn-primary">Write Post</a>
</div>

<div class="table-section">
    <table class="data-table">
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
            {% for post in posts %}
            <tr>
                <td>
                    {% if post.cover_image %}
                    <img src="{{ post.cover_image.url }}" alt="{{ post.title }}" style="width:80px; height:50px; object-fit:cover; border-radius:4px;">
                    {% else %}
                    <div style="width:80px; height:50px; background:#eee; border-radius:4px;"></div>
                    {% endif %}
                </td>
                <td style="max-width:300px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                    {{ post.title }}
                </td>
                <td>
                    <span class="badge {{ post.status }}">{{ post.status|title }}</span>
                </td>
                <td>
                    {% if post.published_at %}{{ post.published_at|date:"M d, Y" }}{% else %}{{ post.created_at|date:"M d, Y" }}{% endif %}
                </td>
                <td>
                    <a href="{% url 'blog_edit' post.pk %}" class="btn btn-small btn-outline-forest">Edit</a>
                    <form method="POST" action="{% url 'blog_delete' post.pk %}" style="display:inline-block;" onsubmit="return confirm('Are you sure you want to delete this post?');">
                        {% csrf_token %}
                        <button type="submit" class="btn btn-small btn-outline-danger">Delete</button>
                    </form>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="5" style="text-align:center; padding: 24px;">No posts found</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}
"""

files_to_write["templates/dashboard/blog/form.html"] = """{% extends 'dashboard/base_dashboard.html' %}

{% block page_title %}{{ title }}{% endblock %}

{% block content %}
<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    <div style="background:white; padding:32px; border-radius:var(--radius); box-shadow:var(--shadow);">
        
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:24px;">
            <div style="flex:1; margin-right:32px;">
                {{ form.title }}
            </div>
            <div class="status-toggle">
                <input type="radio" name="{{ form.status.name }}" value="draft" id="status_draft" {% if form.status.value == 'draft' or not form.status.value %}checked{% endif %}>
                <label for="status_draft">Draft</label>
                
                <input type="radio" name="{{ form.status.name }}" value="published" id="status_published" {% if form.status.value == 'published' %}checked{% endif %}>
                <label for="status_published">Published</label>
            </div>
        </div>

        <div class="summernote-wrapper" style="margin-bottom:24px;">
            {{ form.content }}
        </div>
        
        <div class="form-group" style="margin-bottom:24px;">
            <label>Cover Image</label>
            <label for="{{ form.cover_image.id_for_label }}" class="image-upload-area" id="drop-area" style="min-height:150px; padding:20px;">
                <span>Click or drag image to upload</span>
                <img id="image-preview" class="image-preview" {% if object and object.cover_image %}src="{{ object.cover_image.url }}" style="display:block;"{% endif %}>
            </label>
            <div style="display:none;">{{ form.cover_image }}</div>
            {{ form.cover_image.errors }}
        </div>
        
        <div style="text-align:right;">
            <a href="{% url 'blog_list' %}" class="btn btn-text" style="margin-right:16px;">Cancel</a>
            <button type="submit" class="btn btn-primary" style="padding: 12px 32px;">Save Post</button>
        </div>
    </div>
</form>
{% endblock %}

{% block scripts %}
<script>
    document.querySelector('input[name="title"]').classList.add('blog-title-input');
    document.querySelector('input[name="title"]').placeholder = "Enter Post Title...";

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

files_to_write["templates/dashboard/about.html"] = """{% extends 'dashboard/base_dashboard.html' %}

{% block page_title %}About Us Editor{% endblock %}

{% block content %}
<form method="POST" enctype="multipart/form-data" id="aboutForm">
    {% csrf_token %}
    <input type="hidden" name="delete_members" id="delete_members" value="">
    
    <div style="background:white; padding:28px; border-radius:var(--radius); box-shadow:var(--shadow); margin-bottom:24px;">
        <h3 class="section-title">Hero Content</h3>
        <div class="form-group">
            <label>Tagline</label>
            <input type="text" name="tagline" class="form-control" value="{{ about.tagline|default:'' }}">
        </div>
        <div class="form-group">
            <label>Company Story (Shown in About Body)</label>
            <div class="summernote-wrapper">
                <textarea name="company_story" class="form-control">{{ about.company_story|default:'' }}</textarea>
            </div>
        </div>
        <div class="form-group">
            <label>Mission Statement</label>
            <textarea name="mission_statement" class="form-control" style="min-height:80px;">{{ about.mission_statement|default:'' }}</textarea>
        </div>
    </div>

    <div class="stats-grid-about">
        <div class="form-group" style="text-align:center;">
            <label>Happy Trekkers</label>
            <input type="number" name="stat_trekkers" class="form-control" value="{{ about.stat_trekkers }}" style="text-align:center; font-size:1.5rem; font-family:var(--font-display);">
        </div>
        <div class="form-group" style="text-align:center;">
            <label>Total Vehicles</label>
            <input type="number" name="stat_vehicles" class="form-control" value="{{ about.stat_vehicles }}" style="text-align:center; font-size:1.5rem; font-family:var(--font-display);">
        </div>
        <div class="form-group" style="text-align:center;">
            <label>Equipment Items</label>
            <input type="number" name="stat_equipment" class="form-control" value="{{ about.stat_equipment }}" style="text-align:center; font-size:1.5rem; font-family:var(--font-display);">
        </div>
    </div>

    <h3 class="section-title">Team Members</h3>
    <div class="team-grid" id="members-container">
        {% for member in team_members %}
        <div class="member-card" id="member_card_{{ member.id }}">
            <button type="button" class="btn-remove-member" onclick="removeExistingMember({{ member.id }})">&times;</button>
            <div>
                <label for="member_{{ member.id }}_photo_input" style="cursor:pointer; display:block;">
                    {% if member.photo %}
                    <img src="{{ member.photo.url }}" class="member-photo" id="member_{{ member.id }}_preview">
                    {% else %}
                    <div class="member-photo" style="background:#eee;" id="member_{{ member.id }}_preview"></div>
                    {% endif %}
                </label>
                <input type="file" name="member_{{ member.id }}_photo" id="member_{{ member.id }}_photo_input" style="display:none;" onchange="previewMemberImage(this, 'member_{{ member.id }}_preview')">
            </div>
            <div>
                <input type="text" name="member_{{ member.id }}_name" class="form-control" placeholder="Name" value="{{ member.name }}" style="margin-bottom:8px;">
                <input type="text" name="member_{{ member.id }}_role" class="form-control" placeholder="Role" value="{{ member.role }}" style="margin-bottom:8px;">
                <input type="text" name="member_{{ member.id }}_fav" class="form-control" placeholder="Favorite Trek" value="{{ member.favorite_trek }}" style="margin-bottom:8px;">
                <textarea name="member_{{ member.id }}_bio" class="form-control" placeholder="Bio" style="min-height:60px;">{{ member.bio }}</textarea>
            </div>
        </div>
        {% endfor %}
    </div>
    
    <button type="button" class="btn-add-member" onclick="addMember()">+ Add Team Member</button>
    
    <div style="margin-top:40px; text-align:right;">
        <button type="submit" class="btn btn-secondary" style="background:var(--gold); padding: 14px 40px; font-size:1rem;">Save All Changes</button>
    </div>
</form>
{% endblock %}

{% block scripts %}
<script>
    let newMemberCount = 0;
    const deleteInput = document.getElementById('delete_members');
    
    function removeExistingMember(id) {
        if(confirm('Remove this team member?')) {
            document.getElementById('member_card_' + id).style.display = 'none';
            let current = deleteInput.value;
            deleteInput.value = current ? current + ',' + id : id;
        }
    }

    function removeNewMember(btn) {
        btn.closest('.member-card').remove();
    }

    function addMember() {
        newMemberCount++;
        const card = document.createElement('div');
        card.className = 'member-card';
        card.innerHTML = `
            <button type="button" class="btn-remove-member" onclick="removeNewMember(this)">&times;</button>
            <div>
                <label for="new_member_photo_${newMemberCount}" style="cursor:pointer; display:block;">
                    <div class="member-photo" style="background:#eee; display:flex; align-items:center; justify-content:center; text-align:center; font-size:0.7rem; color:gray;" id="new_member_preview_${newMemberCount}">Upload Photo</div>
                </label>
                <input type="file" name="new_member_photo_${newMemberCount}" id="new_member_photo_${newMemberCount}" style="display:none;" onchange="previewMemberImage(this, 'new_member_preview_${newMemberCount}')">
            </div>
            <div>
                <input type="text" name="new_member_name_${newMemberCount}" class="form-control" placeholder="Name" required style="margin-bottom:8px;">
                <input type="text" name="new_member_role_${newMemberCount}" class="form-control" placeholder="Role" style="margin-bottom:8px;">
                <input type="text" name="new_member_fav_${newMemberCount}" class="form-control" placeholder="Favorite Trek" style="margin-bottom:8px;">
                <textarea name="new_member_bio_${newMemberCount}" class="form-control" placeholder="Bio" style="min-height:60px;"></textarea>
            </div>
        `;
        document.getElementById('members-container').appendChild(card);
    }

    function previewMemberImage(input, previewId) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = document.getElementById(previewId);
                if (preview.tagName === 'IMG') {
                    preview.src = e.target.result;
                } else {
                    const img = document.createElement('img');
                    img.className = 'member-photo';
                    img.id = previewId;
                    img.src = e.target.result;
                    preview.replaceWith(img);
                }
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
</script>
<!-- Summernote Init could be done here if needed manually, or rendered via form widget -->
{% endblock %}
"""

files_to_write["templates/dashboard/contact.html"] = """{% extends 'dashboard/base_dashboard.html' %}

{% block page_title %}Contact Information{% endblock %}

{% block content %}
<form method="POST">
    {% csrf_token %}
    <div class="form-grid">
        <div class="form-left-col">
            <h3 class="section-title">Site Settings</h3>
            <div class="form-group">
                <label>Phone Number</label>
                <input type="text" name="phone" class="form-control" value="{{ settings.phone }}">
            </div>
            <div class="form-group">
                <label>WhatsApp Number</label>
                <input type="text" name="whatsapp" class="form-control" value="{{ settings.whatsapp }}">
            </div>
            <div class="form-group">
                <label>Email Address</label>
                <input type="email" name="email" class="form-control" value="{{ settings.email }}">
            </div>
            <div class="form-group">
                <label>Physical Address</label>
                <textarea name="address" class="form-control" style="min-height:80px;">{{ settings.address }}</textarea>
            </div>
            <div class="form-group">
                <label>Opening Hours</label>
                <textarea name="opening_hours" class="form-control" style="min-height:80px;">{{ settings.opening_hours }}</textarea>
            </div>
        </div>

        <div class="form-right-col">
            <h3 class="section-title">Maps Preview</h3>
            <div class="form-group">
                <label>Maps Embed URL (iframe src)</label>
                <input type="text" name="maps_embed" id="maps-input" class="form-control" value="{{ settings.maps_embed }}">
                <p style="font-size:0.75rem; color:var(--mist); margin-top:4px;">Copy the src attribute from Google Maps embed code.</p>
            </div>
            <div style="border:1px solid var(--border); border-radius:var(--radius); overflow:hidden; height:300px; background:#eee;">
                <iframe id="maps-preview" style="width:100%; height:100%; border:none;" src="{{ settings.maps_embed }}"></iframe>
            </div>
            
            <button type="submit" class="btn btn-primary" style="width:100%; margin-top:32px; padding:14px; font-size:1rem;">Save Contact Info</button>
        </div>
    </div>
</form>
{% endblock %}

{% block scripts %}
<script>
    document.getElementById('maps-input').addEventListener('input', function() {
        document.getElementById('maps-preview').src = this.value;
    });
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
