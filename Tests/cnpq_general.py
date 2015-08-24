#this is a comment to test git
import sys
import snmp_utils

class cnpq_general(object):

	def __init__(self):
		self.ip = ''
		self.aucFileName = ''

	def open_file(self,input_file):
		self.auc_file_open = open(input_file, 'r')
		self.auc_file = self.auc_file_open.read().split("\n")

	def auc_checker(self,ip_address,aucFileName):
		self.open_file(aucFileName)
		self.ip_address = ip_address.split(" ")
		for ip in self.ip_address:
			self.am_list = list()
			self.am_part_num_list = list()
			self.am_sw_list = list()
			self.auc_am_sw_list = list()
			self.part_num_not_in_auc = list()
			self.am_part_num_list_new = list()
			self.auc_am_sw_list_new = list()
			self.sys_desc = list()
			self.output = snmp_utils.performSNMPWalk(ip, ".1.3.6.1.4.1.664.5.13.2.4")
			self.output = self.output[0]
			#print self.output
			self.value = self.output.split("\n")
			#print self.value
			self.sys_desc = snmp_utils.performSNMPWalk(ip, ".1.3.6.1.2.1.1.1")
			#print self.sys_desc[0]
			if "TA5004" not in self.sys_desc[0]:
				#print "TA5000 shelf"
				for line in self.value:
					if line.startswith("SNMPv2-SMI::enterprises.664.5.13.2.4.1.1.") or line.startswith("iso.3.6.1.4.1.664.5.13.2.4.1.1."):
						line = line.split("\"")
						#print line[1]
						self.am_list.append(line[1])
						#print am_list
					elif line.startswith("SNMPv2-SMI::enterprises.664.5.13.2.4.1.2.") or line.startswith("iso.3.6.1.4.1.664.5.13.2.4.1.2."):
						line = line.split("\"")
						#print line[1]
						self.am_part_num_list.append(line[1])
						#print am_part_num_list
					elif line.startswith("SNMPv2-SMI::enterprises.664.5.13.2.4.1.6.") or line.startswith("iso.3.6.1.4.1.664.5.13.2.4.1.6."):
						line = line.split("\"")
						#print line[1]
						self.am_sw_list.append(line[1])
						#print am_sw_list
			else:
				#print "TA5004 shelf not supported yet"
				for line in self.value:
					if line.startswith("SNMPv2-SMI::enterprises.664.5.13.2.4.1.1.") or line.startswith("iso.3.6.1.4.1.664.5.13.2.4.1.6."):
						#print line
						line = line.split("\"")
						#print line[1]
						self.am_list.append(line[1])
						#print self.am_list
					elif line.startswith("SNMPv2-SMI::enterprises.664.5.13.2.4.1.2.") or line.startswith("iso.3.6.1.4.1.664.5.13.2.4.1.6."):
						#print line
						line = line.split("\"")
						#print line[1]
						self.am_part_num_list.append(line[1])
						#print am_part_num_list
					elif line.startswith("SNMPv2-SMI::enterprises.664.5.13.2.4.1.6.") or line.startswith("iso.3.6.1.4.1.664.5.13.2.4.1.6."):
						#print line
						line = line.split("\"")
						#print line[1]
						self.am_sw_list.append(line[1])
						#print am_sw_list

				#TID
				#output = snmp_utils.performSNMPWalk(ip, ".1.3.6.1.2.1.1.5")
				#need to add the -SM and -SCM for TA5004
				for module_index in range(0, len(self.am_list)):
					if self.am_list[module_index] == "SwitchModule":
						self.am_part_num_list[module_index] = self.am_part_num_list[module_index] + '-SM'
					elif self.am_list[module_index] == "SCM":
						self.am_part_num_list[module_index] = self.am_part_num_list[module_index] + '-SCM'

				#print self.am_part_num_list
				#print self.am_sw_list

			#TID
			#output = snmp_utils.performSNMPWalk(ip, ".1.3.6.1.2.1.1.5")

			###Get sw version list from AUC file###
			for part_num in self.am_part_num_list:
				for auc_line in self.auc_file:
					if "ModuleSpec = {0},".format(part_num) in auc_line:
						auc_am_sw = auc_line.split(",")
						self.auc_am_sw_list.append(auc_am_sw[2])
						self.am_part_num_list_new.append(part_num)

			#get a list of part numbers from the shelf that were not found in AUC file
			for part_num_am in self.am_part_num_list:
				if part_num_am not in self.am_part_num_list_new:
					self.part_num_not_in_auc.append(part_num_am)

			#remove sw version associated with part_num not found in auc file
			for part_num_not_found in self.part_num_not_in_auc:
				del self.am_sw_list[self.am_part_num_list.index(part_num_not_found)]

			#trim off some whitespace
			self.auc_am_sw_list = [x.strip() for x in self.auc_am_sw_list]
			#print "full am sw list"
			#print am_sw_list
			#print "auc sw list"
			#print auc_am_sw_list
			#print "full part num list"
			#print am_part_num_list
			#print "those part nums not found in auc"
			#print part_num_not_in_auc
			#print "new part num list"
			#print am_part_num_list_new
			#print len(part_num_not_in_auc)
			#print len(auc_am_sw_list)
			#print len(am_sw_list)
			for i in range(0, len(self.am_sw_list)):
				if self.auc_am_sw_list[i] == self.am_sw_list[i]:
					print "[{0}]: Part number {1} - Expected SW version {2}; actual SW version {3}".format(ip,self.am_part_num_list_new[i],self.auc_am_sw_list[i],self.am_sw_list[i])
				elif self.auc_am_sw_list[i] == "NotApplicable":
					print "[{0}]: Part number {1} - {2}".format(ip,self.am_part_num_list_new[i],self.auc_am_sw_list[i])
				else:
					print "[{0}]: Part number {1} - Expected SW version {2}; actual SW version {3} - FAIL".format(ip,self.am_part_num_list_new[i],self.auc_am_sw_list[i],self.am_sw_list[i])
			for m in range(0, len(self.part_num_not_in_auc)):
				print "[{0}]: Part number {1} - Not found in AUC - FAIL".format(ip,self.part_num_not_in_auc[m])
