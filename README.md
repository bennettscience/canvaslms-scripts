## Canvas LMS Scripts

This repo is a collection of scripts I use regularly when working in Canvas.
Some of them are for admin purposes, others are for course management and
pulling out some student data that is hard to get from the admin or course
tools.

## Using Scripts

To use any of the Python scripts, use `pip install -r requirements.txt` to
install `canvasapi` and dependencies. You should do this is a virtual
environment, if possible. Type annotations are Python 3.7+, but scripts _should_
work in 3.6+. The `canvasapi` library is 3.6+ only.

## Contributions

`pip install -r requirements-dev.txt` to install development packages. `mypy`,
`black`, and `flake8` are for type checks and linting. I don't have many
unittests because many of these scripts are one-offs and not too complex. For
more complicated tools (like `assignment_rubrics`), I do have some tests in
place to check the returned dictionary structure.

This is open for contributions if you have scripts you'd like to share. Open a
PR with the script file and an updated README with a short description of what
it does.

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

#### score_all_submissions

This will fill in a score for an assignment if a submission is present. This is
helpful if you want to give credit for completion without having to load the
gradebook or go through the SpeedGrader.
