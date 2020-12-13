## Canvas LMS Scripts

This repo is a collection of scripts I use regularly when working in Canvas.
Some of them are for admin purposes, others are for course management and
pulling out some student data that is hard to get from the admin or course
tools.

### Scripts

#### assignment_rubrics

This specifies an assignment and returns a list of user scores with any rubric
scores for that assignment. Only Outcomes linked to rubrics are returned.

**Return structure**

```javascript
	{
		[
			'id': 1234,
			'name': 'Last, First',
			'rubric': {
				'123_456': {
					'comments': '',
					'points': 3.0,
					'rating_id': '7364_2363'
				},
				'987_654': {
					'comments': '',
					'points': 1.0,
					'rating_id': '7364_4639'
				},
			'score': 92.0
			}
		...]
	}
```

#### associate_blueprint

From an Instructure course.csv, batch-associate courses to a blueprint course
without needing an SIS ID.

#### canvas_postman

Create a JSON file of all Canvas API methods which can be imported into a
Postman collection.

#### copy_enrollments

Duplicate an entire course's enrollments into a new course shell without
requiring users to accept a new course invitation.

#### course_average

Calculate the average score in a course or a section.

#### create_dummy_students

Quickly create several test students without linking them to an email address.
Useful if you need throwaway accounts for demonstrations or testing.

#### quick_enroll_no_confirm

Because dummy students don't have emails, they can't accept course invitations.
This script will enroll students (users) into any course without sending a
confirmation or requiring them to accept an invitation.
