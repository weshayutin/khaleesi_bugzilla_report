source auth
source team

rm -Rf /tmp/khaleesi
pushd /tmp/; git clone https://github.com/redhat-openstack/khaleesi.git
popd
pushd /tmp/khaleesi/playbooks/; egrep -rn rhbz | sed 's/.*rhbz//' | cut -b 1-7 | sort | uniq > /tmp/buglist
popd
pwd
python3 ospd_eng_bug_report.py
