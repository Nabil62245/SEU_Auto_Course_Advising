
import time

try:
    import requests
except ImportError:
    import os
    os.system('pip install requests')
    import requests


def login(username, password):
    print("\n🔐 Attempting to log in...\n")
    headers = {
        'sec-ch-ua-platform': '"Windows"',
        'Referer': '',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'observe': 'response',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'DNT': '1',
        'Content-Type': 'application/json',
    }

    json_data = {
        'username': username,
        'password': password,
        'browser': 'Chrome',
        'os': 'Windows',
        'agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
        'ip': 'undetected',
        'deviceType': 'Desktop',
        'deviceBrand': 'undetected',
        'deviceModel': 'undetected',
        'deviceResolution': '1920*1080',
        'deviceBrowserResolution': '913*1003',
        'isp': 'undetected',
        'city': 'undetected',
        'country': 'undetected',
        'location': 'undetected',
        'timeZone': 'Asia/Dhaka',
        'attemptCount': 0,
        'rememberMe': True,
    }

    response = requests.post('https://ums-api-service.seu.edu.bd/auth/v/2.0.0/sign-in', headers=headers, json=json_data)
    if response.json().get('code') == "200":
        print('✅ Login Successful!\n')
        name = response.json().get('data', {}).get('name', '')
        token = response.json().get('data', {}).get('token', '')
        return token, name
    else:
        print('Login Failed:', response.text)
        return None, None

def get_course_info(token, course_to_add=None):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    }

    response = requests.get(
        'https://ums-api-service.seu.edu.bd/academic/v/2.0.0/course-advising/advising-table',
        headers=headers
    )

    if response.status_code != 200:
        print("\n❌ Failed to retrieve course information.")
        return []

    print("✅ Offered course list fetched successfully!")

    data = response.json().get('data', {})
    courses = data.get('offeredSectionList', [])

    if not courses:
        print("\n⚠ No offered courses found.")
        return []

    course_list = []  # <-- Initialize once at the top

    if course_to_add:  # automatic course adding
        for course_input in course_to_add:
            matched = False
            for c in courses:
                course_code = f"{c.get('code', '')}.{c.get('sectionNumber', '')}"
                if course_input.upper() == course_code.upper():
                    matched = True
                    print("\n----------------------------------------")
                    print("✅ Course Added To Checklist!")
                    print(f"Course Code : {course_code}")
                    print(f"Course Title: {c.get('title')}")
                    print(f"Faculty     : {c.get('faculty')}")
                    print("Schedule(s) :")
                    schedule_list = c.get('scheduleList', [])
                    if isinstance(schedule_list, list):
                        for s in schedule_list:
                            print(f"  - {s}")
                    else:
                        print("  N/A")
                    print("----------------------------------------")

                    course_list.append({
                        'courseCode': c.get('code'),
                        'section': str(c.get('sectionNumber')),
                        'token1': c.get('token1'),
                        'token2': c.get('token2'),
                    })
                    break
            if not matched:
                print(f"❌ Course {course_input} not found in the offered sections.")

        return course_list  # <-- Return after automatic add

    else:  # interactive input
        try:
            course_count = int(input("\nHow many courses do you want to enroll in? \nCourse Count: "))
        except ValueError:
            print("Invalid number input.")
            return []

        while len(course_list) < course_count:
            i = len(course_list)
            course = input(f"\nEnter course code {i+1} with section (e.g. MAT223.3): ").strip()
            matched = False
            for c in courses:
                course_code = f"{c.get('code', '')}.{c.get('sectionNumber', '')}"
                if course.upper() == course_code.upper():
                    matched = True
                    print("\n----------------------------------------")
                    print("✅ Course Added To Checklist!")
                    print(f"Course Code : {course_code}")
                    print(f"Course Title: {c.get('title')}")
                    print(f"Faculty     : {c.get('faculty')}")
                    print("Schedule(s) :")
                    schedule_list = c.get('scheduleList', [])
                    if isinstance(schedule_list, list):
                        for s in schedule_list:
                            print(f"  - {s}")
                    else:
                        print("  N/A")
                    print("----------------------------------------")

                    course_list.append({
                        'courseCode': c.get('code'),
                        'section': str(c.get('sectionNumber')),
                        'token1': c.get('token1'),
                        'token2': c.get('token2'),
                    })
                    break

            if not matched:
                print("❌ Course not found in the offered sections.")

        print("\nAll selected courses have been added to checking list successfully!")
        print("="*50)
        return course_list


def add_course(token, course):
    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://ums.seu.edu.bd',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    }

    print(f"\n📘 Attempting to add course: {course['courseCode']}.{course['section']}")
    response = requests.post(
        'https://ums-api-service.seu.edu.bd/academic/v/2.0.0/course-advising/add-drop',
        headers=headers,
        json=course
    )

    try:
        return response.json()
    except Exception:
        print(f"⚠️ Invalid JSON response for {course['courseCode']}. Response: {response.text}")
        return {"data": [{"status": "error", "message": "Invalid response"}]}







def main(username=None, password=None, course_to_add=None):

    print("=" * 50)
    print("🎓  SEU Course Advising Automation")
    print("=" * 50)

    token, name = login(username, password)
    if not token:
        print("❌ Login failed. Please check your credentials.")
        return

    
    print(f"\nWelcome, {name}!")
    print("=" * 50)
    print("\n📚 Fetching available courses...")

    courses = get_course_info(token, course_to_add)
    if not courses:
        print("⚠ No courses found.")
        return

    print("\n----------------------------------------------")
    print("📘 Course Advising Process Started")
    print("----------------------------------------------")

    added_courses = {}
    attempt = 1
    total = len(courses)

    while len(added_courses) < total:
        print(f"\n▶ Attempt #{attempt} | Progress: {len(added_courses)}/{total} added")
        print("-" * 50)

        for course in courses:
            if course['courseCode'] in added_courses:
                continue  # skip already added

            response = add_course(token, course)
            if response["code"] != "200":
                print(f"❌  Error adding course {course['courseCode']}: {response.get('message', 'Unknown error')}")
                time.sleep(2)
                continue

            data = response.get('data', [{}])[0]
            Status = data.get('status', '')
            Msg = data.get('message', '')

            course_code = course.get('courseCode')
            section = course.get('section')

            if Status == 'success':
                print(f"✅  Successfully added {course_code} (Section {section})")
                added_courses[course_code] = course
            else:
                print(f"❌  Failed to add {course_code} (Section {section}) — {Msg}")

            time.sleep(1)

        attempt += 1
        if len(added_courses) < total:
            print("\nWaiting before next retry...\n")
            time.sleep(2)

    print("\n----------------------------------------------")
    print("🎉  All Courses Added Successfully!")
    print("----------------------------------------------")
    print(f"Total Added   : {len(added_courses)} / {total}")
    print(f"Total Attempts: {attempt - 1}")
    print("=" * 50)
    print("✅  Process Completed Successfully.")
    print("=" * 50)


# if __name__ == "__main__":
# course_to_add = ["EEE181.5", "MAT241.4", "ENG103.18", "CSE241.5"]
course_to_add = None  # for interactive input, leave this list empty

USERNAME = "" or input("Enter your SEU username: ").strip()
PASSWORD = "" or input("Enter your SEU password: ").strip()

main(USERNAME, PASSWORD, course_to_add)
