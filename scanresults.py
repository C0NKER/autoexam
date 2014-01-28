import os
import json

def enum(**enums):
    return type('Enum', (), enums)

WarningTypes = enum(MULT_SELECTION = "Multiple Selection",UNCERTANTY = "Uncertainty");

class Report(object):
    """Class to represent the scan report"""
    def __init__(self):
        self.errors = []
        self.success = False
        self.test = None

class Warning(object):
    """Warnings"""
    def __init__(self, question, selection, wtype):
        self.question = question
        self.selection = selection
        self.wtype = wtype

    def __str__(self):
        if self.wtype == WarningTypes.UNCERTANTY:
            return "The selection of the answer %s in question %d is uncertain"%(self.selection, self.question) 
        elif self.wtype == WarningTypes.MULT_SELECTION:
            return "Is possible that the question %d has additional selections. Possible values %s"%(self.question,self.selection) 

    def to_dict(self):
        return {'type': self.wtype, 'question': self.question, 'selection': self.selection, 'message': self.__str__() }

    @classmethod
    def load_from_json(cls,json):
        return Warning(json["question"],json["selection"],json["type"])

class QrcodeError(object):
    """QRCode error class"""
    def __str__(self):
        return "There was an error with the detection of the QRCode"   

class MarkersError(object):
    """Marker error class"""
    def __str__(self):
        return "There was an error with the detection of the markers"   
          
class QuestionError(object):
    """docstring for QuestionError"""
    def __init__(self, q, msg):
        self.question = q
        self.message = msg

    def __str__(self):
        return self.message + " in question %d"%self.question

class Question:
    """Question Class"""
    def __init__(self, id, total_answers, multiple, answers = []):
        self.answers = answers
        self.total_answers = total_answers  
        self.multiple = multiple
        self.id = id

    @classmethod
    def load_from_json(cls,json):
        return Question(json["id"],json["total_answers"],json["multiple"],json["answers"])

    def to_dict(self):
        result = {}
        result["id"] = self.id
        result["answers"] = self.answers
        result["total_answers"] = self.total_answers
        result["multiple"] = self.multiple
        return result
        
class Test(object):
    """Test class"""
    def __init__(self, exam_id, id, questions, warnings={}):              
        self.exam_id = exam_id
        self.id = id
        self.questions = questions
        self.warnings = warnings

    @classmethod
    def load_from_json(cls,json):
        questions = {}
        for k,v in json["questions"].items():
            questions[int(k)] = Question.load_from_json(v)
        
        warnings = [Warning.load_from_json(w) for w in json["warnings"]]

        return Test(json["exam_id"],json["id"],questions, warnings)


    def __str__(self):
        result = "Exam ID: %s\nTest ID: %s\nTotal Questions: %d\n"%(self.exam_id,self.id,len(self.questions))
        for (k,v) in self.questions.items():            
            result+="%d -> %s\n"%(k,v.answers)
        for w in self.warnings:            
            result+="%s\n"%(w)

        return result

    def __eq__(self,other):
        return self.exam_id == other.exam_id and self.id==other.id and self.questions == other.questions

    def __ne__(self,other):
        return not self.__eq__(other)

    def to_dict(self):
        result = {}
        result["exam_id"] = self.exam_id
        result["id"] = self.id
        result["questions"] = {}
        for k,v in self.questions.items():
            result["questions"][k]=v.to_dict()
        result["warnings"] = [w.to_dict() for w in self.warnings]
        return result

def dump(tests, filename, overwrite = False):
    to_serialize = {}
    all_tests = {}
    #restore previous tests if file exists...
    if not overwrite and os.path.exists(filename):
        print('Restoring previous tests...')
        all_tests = parse(filename)
    #include the new tests...
    for (k,v) in tests.items():
        all_tests[k]=v
    #transform objects to dictionaries to store them in json format
    for (k,v) in all_tests.items():
        print('Saving test: {0}'.format(k))
        to_serialize[k]=v.to_dict();
    #dump in json format
    f = file(filename,'w') 
    json.dump(to_serialize, f) 
    f.close()

def parse(filename):
    if os.path.exists(filename):
        tests = {}
        f = open(filename, 'r')
        content = json.loads(f.read())
        f.close()

        for k,v in content.items():
            tests[int(k)] = Test.load_from_json(v)

        return tests

def dump_single(test,file_prefix="test_"):
    f = file(file_prefix+str(test.id)+".json",'w') 
    json.dump(test.to_dict(), f) 
    f.close()

def parse_single(filename):
    if os.path.exists(filename):
        f = open(filename, 'r')
        content = json.loads(f.read())
        f.close()

        return Test.load_from_json(content)





