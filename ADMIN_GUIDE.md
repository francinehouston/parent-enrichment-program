# Admin System Guide

## Overview

The admin system allows you to manage all content for the Parent Enrichment Program, including documents, courses, quizzes, videos, tests, and certifications.

## Accessing the Admin Area

1. Navigate to `/admin/login` or click "Admin Login" in the navigation menu
2. **Default Credentials:**
   - Username: `admin`
   - Password: `admin123`

⚠️ **IMPORTANT:** Change the default password in production! Edit `app.py` and update the `ADMIN_CREDENTIALS` dictionary.

## Features

### 1. Documents
- Create text documents with categories
- Organize by category (General, Parenting Tips, Child Development, Resources, Guides)
- View and manage all documents

### 2. Online Courses
- Create structured courses with descriptions
- Set difficulty levels (Beginner, Intermediate, Advanced)
- Add duration information
- Include detailed course content

### 3. Quizzes
- Create interactive quizzes with multiple-choice questions
- Add unlimited questions dynamically
- Set time limits (optional)
- Mark correct answers for each question

### 4. Videos
- Add video content via URLs (YouTube, Vimeo, or direct links)
- Include descriptions and thumbnails
- Categorize videos
- Videos are automatically embedded when viewing

### 5. Tests
- Create comprehensive tests with scoring
- Add multiple-choice questions with point values
- Set passing scores (percentage)
- Configure time limits
- Track total points

### 6. Certifications
- Create certification programs
- Define requirements for earning certifications
- Set validity periods
- Link to associated courses

## Usage Tips

### Creating Quizzes and Tests
1. Click "Add Question" to add questions dynamically
2. Fill in the question text and options
3. Select the correct answer from the dropdown
4. For tests, assign point values to each question
5. Remove questions using the "Remove Question" button

### Adding Videos
- **YouTube:** Paste the full URL (e.g., `https://www.youtube.com/watch?v=VIDEO_ID`)
- **Vimeo:** Paste the full URL (e.g., `https://vimeo.com/VIDEO_ID`)
- **Direct links:** Use direct video file URLs (MP4, etc.)

### Dashboard
The admin dashboard provides:
- Quick overview of all content counts
- Quick action buttons to create new content
- Easy navigation to all content types

## Security Notes

1. **Change Default Password:** Update `ADMIN_CREDENTIALS` in `app.py`
2. **Session Management:** Admin sessions are stored in Flask sessions
3. **Production:** Consider using environment variables for credentials
4. **Database:** In production, migrate from in-memory storage to a proper database

## Future Enhancements

Consider adding:
- User management (multiple admins)
- Content editing and deletion
- Content publishing/unpublishing
- Analytics and reporting
- File uploads for documents and videos
- Rich text editor for content creation
- Content search functionality




