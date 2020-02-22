from django.db import models

class TempTeam(models.Model):
    tname = models.CharField(max_length=20)
    indId = models.IntegerField()
    tdevopsRatio = models.IntegerField()
    tdesignRatio = models.IntegerField()
    tavgCost = models.IntegerField()
    tOnOffRatio = models.IntegerField()
    tratioGtAvgExp = models.IntegerField()
    tAvgNoOfPto = models.IntegerField()
    tAvgSkillLevel = models.IntegerField()
    tCntdistinctskills = models.IntegerField()
    tFitnessValue = models.CharField(max_length=20)

class IndConsidered2(models.Model):
    indId= models.IntegerField()

class Individuals(models.Model):
    indId              = models.IntegerField()
    indTname           = models.CharField(max_length=20)
    indExp             = models.CharField(max_length=20)
    indCost            = models.CharField(max_length=20)
    indSite            = models.CharField(max_length=20)
    indRole            = models.CharField(max_length=20)
    indOnoroff         = models.CharField(max_length=20)
    indThxNotesG       = models.CharField(max_length=20)
    indThxNotesR       = models.CharField(max_length=20)
    indGrade           = models.CharField(max_length=20)
    indNoPto           = models.CharField(max_length=20)
    indDoj             = models.DateField()
    indSkillLevel      = models.CharField(max_length=20)
    indSkill           = models.CharField(max_length=20)

class Prjnumbers(models.Model):
    prjID = models.AutoField(primary_key=True)
    tag=models.CharField(max_length=3,default='prj')

