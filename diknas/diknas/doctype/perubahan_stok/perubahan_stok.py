# -*- coding: utf-8 -*-
# Copyright (c) 2018, Bobby and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import  flt,cint

class PerubahanStok(Document):
	def validate(self):
		if cint(self.qty)<0:
			#check kartu stock
			ks = frappe.db.sql("""select name, sekolah,jenis_barang,qty from `tabKartu Stok` where sekolah="{}" and jenis_barang="{}" """.format(self.sekolah,self.jenis_barang),as_list=1)
			ada=0
			for n in ks:
				ada=1
				if cint(n[2])<cint(self.qty)*-1:
					frappe.throw("Stock di sekolah {} untuk {} hanya ada {}".format(self.sekolah, self.jenis_barang,cint(n[2])+cint(self.qty)))
			if ada==0:
				doc = frappe.get_doc({
					"doctype": "Kartu Stok",
					"jenis_barang":self.jenis_barang,
					"qty":0,
					"sekolah":self.sekolah
					})
				doc.insert()
		else :
			ks = frappe.db.sql("""select name, sekolah,jenis_barang,qty from `tabKartu Stok` where sekolah="{}" and jenis_barang="{}" """.format(self.sekolah,self.jenis_barang),as_list=1)
			ada=0
			for n in ks:
				ada=1
			if ada==0:
				doc = frappe.get_doc({
					"doctype": "Kartu Stok",
					"jenis_barang":self.jenis_barang,
					"qty":0,
					"sekolah":self.sekolah
					})
				doc.insert()
	def on_submit(self):
		#check kartu stock
		ks = frappe.db.sql("""update `tabKartu Stok` set qty=qty+({}) where sekolah="{}" and jenis_barang="{}" """.format(self.qty,self.sekolah,self.jenis_barang),as_list=1)				
	def on_cancel(self):
		ks = frappe.db.sql("""update `tabKartu Stok` set qty=qty-({}) where sekolah="{}" and jenis_barang="{}" """.format(self.qty,self.sekolah,self.jenis_barang),as_list=1)				
