#!/usr/bin/env python

class Point:
    
    def __init__(self, p_id, x, y, z, text):
        
        self.p_id= p_id
        self.x=x
        self.y=y
        self.z=z
        self.text=text
        
    def get_coords(self):
        
        coords = {'x': self.x,'y':self.y,'z':self.z}
        return coords
    
    def get_string_of_points(self):
        
        string = str(self.p_id)+" "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" "+str(self.text)
        return string
    
    def dump_point(self):
        
        print self.p_id," ",self.x," ",self.y," ",self.z," ",self.text
    
    def point_to_tuple(self):
        tuplepoint = (self.p_id, self.x, self.y, self.z, self.text)
        return tuplepoint

class PointsList:
    
    def __init__(self):
        
        self.listofpoints = []
        
    def add_point(self, p):
        
        self.listofpoints.append(p)
        
    def add_points(self, lp):
        
        self.listofpoints.extend(lp)
        
    def pid_is_in_lop(self, aux_p_id):
        
        for p in self.listofpoints:
            
            if aux_p_id == p.p_id :
                return True
        
        return False
        
    def list_to_tuple(self):
        
        list_aux=[]
        for p in self.listofpoints:
            list_aux.append(p.point_to_tuple())
        return list_aux

class Data:
    
    def __init__(self):
        pass
        
    def data_from_txt_file(self, filepathname):
        
        file = open(filepathname,'r')
        self.lines = file.readlines()
        file.close()

class TotalStation:
    
    def __init__(self,filename):
        
        self.d = Data()
        self.d.data_from_txt_file(filename)
        self.points = PointsList()
        
    def set_data(self, data):
        
        self.d = data
    
    def get_data(self):
        
        return self.d
    
    def parse_retrieve_data(self):
        
        valid_lines = filter(self.is_point, self.d.lines)
        
        for l in valid_lines:

            self.points.add_point(self.get_point(l))
    
    def is_point(self):
        
        pass
    
    def get_point(self):
        
        pass
    
    def print_found_points(self):
        
        
        for p in self.points.listofpoints:
            p.dump_point()
            
    def export_points_toTXT(self, filepathname):
        
        file = open(filepathname,'w')
        
        for p in self.points.listofpoints:
            
            file.write(p.get_string_of_points()+"\n")
            
        file.close()


class LeicaTCR1205(TotalStation):
    
    def parse_retrieve_data(self):
        
        valid_lines = []
        
        for l in self.d.lines:
            
            if self.is_point(l) == True:

                valid_lines.append(l)

        for l in valid_lines:

            aux = self.get_point(l)
            
            if (self.points.pid_is_in_lop(aux.p_id)) == False :
                
                self.points.add_point(aux)
    
    def is_point(self,line):
        
        tokens = line.split()
        
        try:
            float(tokens[1])
            float(tokens[2])
            float(tokens[3])
        
        except (ValueError, IndexError):
            
            is_point = False
        
        else:    
            #di questo controllo che segue FORSE non gliene frega un beliscimu
            if tokens[4]=="MEAS":
                is_point = True
            else:
                is_point = False
        
        return is_point
        
    def get_point(self,line):
        
        tokens = line.split()
        
        if len(tokens)> 5:
            text = str(tokens[5])
        else:
            text = ""
            
        p = Point(str(tokens[0]), float(tokens[1]), float(tokens[2]), float(tokens[3]), text)
        
        return p

