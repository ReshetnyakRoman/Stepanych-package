import unittest
from Stepanych.models import mainTable

class mainTableModelTestCase(unittest.TestCase):
	def test_password_setter(self):
		team = mainTable(password = 'cat')
		self.assertTrue(team.passwordHash is not None)

	def test_no_password_getter(self):
		team = mainTable(password = 'cat')
		with self.assertRaises(AttributeError):
			team.password

	def test_password_salts_are_random(self):
		team1 = mainTable(password='cat')
		team2 = mainTable(password='cat')
		self.assertTrue(team1.passwordHash != team2.passwordHash)

	def test_genereate_cofirmation_token(self):
		token = mainTable.generate_confirmation_token(36000)
		self.assertTrue(token is not None)
	
	def test_cofirmation(self):
		token = mainTable.generate_confirmation_token(3600)
		data = mainTable.confirm(token)
		self.assertTrue(data == mainTable.keyTeamCompetition)

