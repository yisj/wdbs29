import sys
import os

appid = sys.argv[1]

sh = list()


keytool = 'keytool -genkey -v -keystore keys/%s.jks -keyalg RSA -keysize 2048 -validity 10000 -alias %s' % (appid, appid)
answers = [
	"tmdwotnwls",
	"tmdwotnwls",
	"Gaedog",
	"Gaedog",
	"Gaedog",
	"Seoul",
	"Seoul",
	"KR",
	"Y",
	"tmdwotnwls",
	"tmdwotnwls"
]
answer = "echo '%s'" % '\n'.join(answers)

os.system("%s | %s" % (answer, keytool))