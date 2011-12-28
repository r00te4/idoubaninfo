# -*- coding: utf-8 -*-
import wsgiref.handlers
import cgi
import os
import datetime,time
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import users 
from google.appengine.ext.webapp import template
##here is API not EXT

class Twim(db.Model):
	mid=db.StringProperty(multiline=True)
	content=db.TextProperty()
	title=db.StringProperty(multiline=True)
	tclass=db.StringProperty(multiline=True,choices=set(["niki", "photo","group","event","widget"]))
	date=db.DateTimeProperty(auto_now_add=True)



class MainPage(webapp.RequestHandler):
	def get(self):
		twimclass=self.request.get('class')
		i=13
		p1=i
		if twimclass:
			tquery="SELECT * FROM Twim WHERE tclass=:tclass ORDER BY date DESC LIMIT 15"
			Greetings=db.GqlQuery(tquery,tclass=twimclass)
		else:
			Greetings=db.GqlQuery("SELECT * FROM Twim ORDER BY date DESC LIMIT 15")
		if users.get_current_user():
			url_text='Log off'
			url=users.create_logout_url(self.request.uri)
		else:
			url_text='Log Inn'
			url=users.create_login_url(self.request.uri)
		template_values={'Greetings':Greetings,'url':url,'url_text':url_text,'Nstart':p1}
		path = os.path.join(os.path.dirname(__file__),'index.html')
		self.response.out.write(template.render(path,template_values))

class NextPage(webapp.RequestHandler):
	def get(self):
		i=13
		nfrom=self.request.get('pstart')
		p1=int(nfrom)+i
		nto=str(i)
		p2=p1-2*i
		Greetings=db.GqlQuery("SELECT * FROM Twim ORDER BY date DESC LIMIT "+nfrom+","+nto)
		if users.get_current_user():
			url_text='Log off'
			url=users.create_logout_url(self.request.uri)
		else:
			url_text='Log Inn'
			url=users.create_login_url(self.request.uri)
		template_values={'Greetings':Greetings,'url':url,'url_text':url_text,'Nstart':p1,'Pstart':p2}
		path = os.path.join(os.path.dirname(__file__),'index.html')
		self.response.out.write(template.render(path,template_values))

class ShowMe(webapp.RequestHandler):
	def get(self):
		smid=self.request.get('id')
		smid=str(smid)
		result={}
		showings=db.GqlQuery("SELECT * FROM Twim WHERE mid='"+smid+"'")
		for showing in showings:
			title=showing.title
			content=showing.content
			id=showing.mid
			format="%Y-%m-%d %H:%M:%S"
			dtime=str(showing.date)
			dtime=dtime[:-7]
			dtime=datetime.datetime(*time.strptime(dtime,format)[:6])+datetime.timedelta(hours=8)
		template_values={'title':title,'content':content,'datetime':dtime,'mid':smid}
		path = os.path.join(os.path.dirname(__file__),'show.html')
		self.response.out.write(template.render(path,template_values))
class adminCheck(webapp.RequestHandler):
	def get(self):
		print 'Content-Type:text/html'
		print '<html>Enter The Verify Code Plz!'
		print "<form action='admin' method='post'><input name='password' type='password'><br><input type='submit' value='Sumit'></form></html>"
	def post(self):
		pwd=self.request.get('password')
		if pwd=='idouban':
			print 'Content-Type:text/html'
			mid=0
			ccs=db.GqlQuery("SELECT * FROM Twim ORDER BY  date DESC LIMIT 1")
		        for cc in ccs:
				mid=int(cc.mid)+1
			print 'Ok'
			template_values={'mid':mid}
			path = os.path.join(os.path.dirname(__file__),'admin.html')
			self.response.out.write(template.render(path,template_values))
		else:
			print 'Content-Type:text/html'
			print "Sorry,Password is Wrong"
			print "<form action='admincheck' method='post'><input name='password' type='password'><br><input type='submit' value='Sumit'></form>"
			
class Guestbook(webapp.RequestHandler):
	def post(self):
		twim=Twim()
		twim.content=self.request.get('content')
		twim.title=self.request.get('title')
		twim.tclass=self.request.get('cls')
		twim.mid=str(self.request.get('mid'))
		twim.put()
		self.redirect('/')

def main():
	app=webapp.WSGIApplication([('/',MainPage),('/admin/write',Guestbook),('/nextpage',NextPage),('/show',ShowMe),('/admin',adminCheck)],debug=False)
	wsgiref.handlers.CGIHandler().run(app)

if __name__=="__main__":
	main()













