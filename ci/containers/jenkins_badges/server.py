import sys, jenkins_badges

base_url = sys.argv[1]
# not required username & password because anonymous jenkins user has read access
app = jenkins_badges.create_app(base_url=base_url)
app.run(host="0.0.0.0")