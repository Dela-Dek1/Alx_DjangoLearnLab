from django.contrib.auth.models import User, Group

def create_test_users():
    viewer_user, created = User.objects.get_or_create(
        username='viewer',
        defaults={'email': 'viewer@example.com'}
    )
    if created:
        viewer_user.set_password('viewerpass')
        viewer_user.save()
        viewers_group = Group.objects.get(name='Viewers')
        viewer_user.groups.add(viewers_group)
    
    
    editor_user, created = User.objects.get_or_create(
        username='editor',
        defaults={'email': 'editor@example.com'}
    )
    if created:
        editor_user.set_password('editorpass')
        editor_user.save()
        editors_group = Group.objects.get(name='Editors')
        editor_user.groups.add(editors_group)
    
    
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@example.com'}
    )
    if created:
        admin_user.set_password('adminpass')
        admin_user.save()
        admins_group = Group.objects.get(name='Admins')
        admin_user.groups.add(admins_group)