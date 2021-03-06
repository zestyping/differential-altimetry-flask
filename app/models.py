import datetime
from app import db
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))



class Reading(db.Model):
	sensor_id = db.Column(db.String(64), db.ForeignKey('sensor.sensor_id'), primary_key=True)
	time = db.Column(db.DateTime, primary_key=True)
	calibration = db.Column(db.Boolean())
	height = db.Column(db.Float())
	lat = db.Column(db.Float())
	lon = db.Column(db.Float())
	lat_lon_sd = db.Column(db.Float())
	uncal_pressure = db.Column(db.Float())
	uncal_pressure_sd = db.Column(db.Float())
	uncal_temperature = db.Column(db.Float())
	uncal_temperature_sd = db.Column(db.Float())
	sample_count = db.Column(db.Integer())

	__table_args__ = (db.UniqueConstraint('sensor_id', 'time', name='sensor_time_uc'),)

	def __repr__(self):
		return '<Reading {}>'.format(self.sensor_id, self.time)

	def save(self):
		db.session.add(self)
		db.session.commit()

	def jsonify(self):
		return {'sensor_id':self.sensor_id,
				'calibration':self.calibration,
				'time':self.time,
				'height':self.height,
				'lat': self.lat,
				'lon':self.lon,
				'lat_lon_sd':self.lat_lon_sd,
				'uncal_pressure':self.uncal_pressure,
				'uncal_pressure_sd':self.uncal_pressure_sd,
				'uncal_temprature': self.uncal_temperature,
				'uncal_temprature_sd': self.uncal_temperature_sd,
				'sample_count':self.sample_count}

	def csvify(self):
		return {self.sensor_id,
				self.calibration,self.time,self.duration,
				self.lat,self.lon,self.lat_lon_sd,
				self.uncal_pressure,self.uncal_pressure_sd,
				self.uncal_temperature,self.uncal_temperature_sd,
				self.sample_count}

	@staticmethod
	def saveJson(jsonItem):
		s_id = jsonItem.get('sensor_id')
		time = jsonItem.get('time')
		reading = Reading(sensor_id=s_id,
						  calibration=jsonItem.get('calibration'),
						  time=datetime.datetime.fromtimestamp(time),
						  height=jsonItem.get('height'),
						  lat=jsonItem.get('lat'),
						  lon=jsonItem.get('lon'),
						  lat_lon_sd=jsonItem.get('lat_lon_sd'),
						  uncal_pressure=jsonItem.get('uncal_pressure'),
						  uncal_pressure_sd=jsonItem.get('uncal_pressure_sd'),
						  uncal_temperature=jsonItem.get('uncal_temperature'),
						  uncal_temperature_sd=jsonItem.get('uncal_temperature_sd'),
						  sample_count=jsonItem.get('sample_count'))
		reading.save()
		return reading

	@staticmethod
	def csv_headers(self):
		return {'sensor_id',
				'calibration','time','duration',
				'lat','lon','lat_lon_sd',
				'uncal_pressure','uncal_pressure_sd',
				'uncal_temprature','uncal_temprature_sd',
				'sample_count'}

	@staticmethod
	def get_all():
		return Reading.query.all()

	@staticmethod
	def get_sensor(sensorId, count):
		return Reading.query.filter_by(sensor_id=sensorId).order_by(Reading.time.desc()).limit(count).all()

	@staticmethod
	def get_range(start, end):
		return Reading.query.filter(Reading.time.between(datetime.datetime.fromtimestamp(start),
														 datetime.datetime.fromtimestamp(end)))

	@staticmethod
	def get_sensor_range(sensorId, start, end):
		return Reading.query.filter_by(sensor_id=sensorId).filter(
			Reading.time.between(datetime.datetime.fromtimestamp(start),
								 datetime.datetime.fromtimestamp(end)))



class Sensor(db.Model):
	sensor_id = db.Column(db.String(64), primary_key=True)
	fixed = db.Column(db.Boolean())
	lat = db.Column(db.Float())
	lon = db.Column(db.Float())
	alt = db.Column(db.Float())
	points = db.relationship('Point', backref='sensor', lazy='dynamic')
	readings = db.relationship('Reading', backref='sensor', lazy='dynamic')
	# TODO Add pressure_offset for fixed=false

	def __repr__(self):
		return '<Sensor {}>'.format(self.sensor_id)

	def save(self):
		db.session.add(self)
		db.session.commit()

	def jsonify(self):
		if self.fixed :
			return {'sensor_id':self.sensor_id,
					'fixed':self.fixed,
					'lat':self.lat,
					'lon':self.lon,
					'alt':self.alt}
		else :
			return {'sensor_id':self.sensor_id,
					'fixed':self.fixed}

	def csvify(self):
		return {self.sensor_id, self.fixed, self.lat, self.lon, self.alt}

	@staticmethod
	def csv_headers(self):
		return {'sensor_id', 'fixed', 'latitude', 'longitude', 'elevation'}

	@staticmethod
	def get_all():
		return Sensor.query.all()

	@staticmethod
	def get_all_ids():
		return db.session.query(Sensor.sensor_id).distinct().all()

	@staticmethod
	def get(sensorId):
		return Sensor.query.filter_by(sensor_id=sensorId).first()

	@staticmethod
	def saveJson(jsonReq):
		sensor_id = str(jsonReq.get('sensor_id', ''))
		fixed = jsonReq.get('fixed', False)
		lat = jsonReq.get('lat')
		lon = jsonReq.get('lon')
		alt = jsonReq.get('alt')

		# verify required fields
		if (sensor_id and fixed and lat and lon and alt) or (sensor_id and not fixed):
			# create sensor, save & return
			sensor = Sensor(sensor_id=sensor_id, fixed=fixed, lat=lat, lon=lon, alt=alt)
			sensor.save()
			return sensor

class Point(db.Model):
	id = db.Column(db.String(64), primary_key=True)
	sensor_id = db.Column(db.String(64), db.ForeignKey('sensor.sensor_id'))
	time = db.Column(db.DateTime)
	lat = db.Column(db.Float)
	lon = db.Column(db.Float)
	lat_lon_sd = db.Column(db.Float)
	alt = db.Column(db.Float)
	alt_sd = db.Column(db.Float)

	def __repr__(self):
		return '<Point {}>'.format(self.id)

def add_point(point):
	s_id = point.sensor_id
	sensor = Sensor.query.filter_by(sensor_id=s_id).first()
	if sensor is None:
		sensor = Sensor(sensor_id=s_id, fixed=False)
		sensor.points = [point]
		db.session.add(sensor)
	else:
		db.session.add(point)
	db.session.commit()

def add_points(points):
	s_id = points[0].sensor_id
	sensor = Sensor.query.filter_by(sensor_id=s_id).first()
	if sensor is None:
		sensor = Sensor(sensor_id=s_id, fixed=False)
		sensor.points = points
		db.session.add(sensor)
	else:
		db.session.add_all(points)
	db.session.commit()

