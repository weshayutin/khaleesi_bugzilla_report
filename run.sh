source auth
source team

pushd /tmp/; git clone https://github.com/redhat-openstack/khaleesi.git
popd
pushd /tmp/khaleesi/playbooks/; egrep -rn rhbz | sed 's/.*rhbz//' | cut -b 1-7 > /tmp/buglist
popd
pwd
python3 ospd_eng_bug_report.py
