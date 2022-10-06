
import requests

iq_session = requests.Session()
iq_session.auth = requests.auth.HTTPBasicAuth("admin", "admin123")
iq_session.cookies.set('CLM-CSRF-TOKEN', 'api')
iq_headers = {'X-CSRF-TOKEN': 'api'}
iq_url = "http://localhost:8070"
stages = ["develop","source","build","stage-release","release","operate"]
revoke = True

apps = iq_session.get(f'{iq_url}/api/v2/applications').json()["applications"]
for app in apps:
	publicId = app["publicId"]
	app_id = app["id"]
	print(f'Working on: {publicId}')
	if revoke:
		url = f'{iq_url}/rest/policyViolationGrandfathering/revoke/{publicId}'
		test = iq_session.put(url, headers=iq_headers)
		print(test.status_code)
	reports = iq_session.get(f'{iq_url}/api/v2/reports/applications/{app_id}').json()
	for report in reports:
		stage = report["stage"]
		if stage in stages:
			print(f'--{stage}')
			report_id = report["reportHtmlUrl"].split("/")[-1]
			url = f'{iq_url}/rest/report/{publicId}/{report_id}/reevaluatePolicy'
			result = iq_session.post(url, headers=iq_headers)
			if result.status_code == requests.codes.ok:
				print(f'complete: {result.status_code}')
