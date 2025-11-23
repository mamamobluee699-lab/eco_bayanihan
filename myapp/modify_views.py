import re

# Read the file
with open('views.py', 'r') as f:
    content = f.read()

# Find the second select_event function and add the points notification logic
# Look for the pattern before the return render statement in the second function
pattern = r'(def select_event\(request\):.*?)(    # Check for registration success in session and pass to template\n    registration_success = request\.session\.pop\(\'registration_success\', None\) if request\.method == \'GET\' else None\n\n    context = \{)(.*?return render\(request, \'myapp/select_event\.html\', context\))'

# Replacement with points notification
replacement = r'\1\2\n    \n    # Check for points added notification\n    points_added = None\n    if participant and request.method == \'GET\':\n        points_key = f\'points_added_{participant.email}\'\n        points_added = request.session.pop(points_key, None)\n        if points_added:\n            messages.success(request, f"🎉 {points_added[\'points\']} points have been added! Your total is now {points_added[\'total_points\']} points.")\n\3'

# Apply the replacement with DOTALL flag to match across newlines
new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write back to file
with open('views.py', 'w') as f:
    f.write(new_content)

print("File modified successfully!")
