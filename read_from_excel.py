import win32com.client as winclient

EXCEL_PATH = r"E:\OlympiaCustom\OC_FRIENDLY_1\DE.xlsx"
PPT_PATH = r"E:\OlympiaCustom\OC_FRIENDLY_1\OCF1.pptm"

SLIDE = {
    # Khoi dong
    "KD_CHUNG_1": 5,
    "KD_RIENG_1": 7,
    "KD_RIENG_2": 9,
    "KD_RIENG_3": 11,
    "KD_RIENG_4": 13,
    "KD_CHUNG_2": 15,
    "VCNV": 17,
    # Tang toc
    "TT1": 21,
    "TT2": 23,
    "TT3": 25,
    "TT4": 27,
    "TT5": 29,
    "HS": 33,
    # Ve dich
    # 1
    "VD1_CDND": 38,
    "VD1_NSHV": 40,
    "VD1_CDTL": 44,
    # 2
    "VD2_CDND": 49,
    "VD2_NSHV": 51,
    "VD2_CDTL": 55,
    # 3
    "VD3_CDND": 60,
    "VD3_NSHV": 62,
    "VD3_CDTL": 66,
    # 4
    "VD4_CDND": 71,
    "VD4_NSHV": 73,
    "VD4_CDTL": 77,
    "CHP": 80
}

class Loader():
    def __init__(self, excel_path=EXCEL_PATH, ppt_path=PPT_PATH):
        self.excel_app = winclient.Dispatch("Excel.Application")
        self.workbook = self.excel_app.Workbooks.Open(excel_path)
        self.ppt_app = winclient.Dispatch("PowerPoint.Application")
        self.ppt_app.Visible = True
        self.presentation = self.ppt_app.Presentations.Open(ppt_path)

    def _write(self, sheet_name, cell_address, slide_index, shape_name):
        # Select the sheet
        sheet = self.workbook.Sheets(sheet_name)
        # Read data from the specific cell
        cell_value = sheet.Range(cell_address).Value
        # Select the slide
        slide = self.presentation.Slides(slide_index)
        # Find the shape by name
        shape = None
        for s in slide.Shapes:
            if s.Name == shape_name:
                shape = s
                break
        if shape is None:
            raise ValueError(f"Shape with name '{shape_name}' not found in slide {slide_index}")
        # Write data to the shape
        shape.TextFrame.TextRange.Text = cell_value


    def load_kd(self):
        sheet_name = "KD"
        # KD_CHUNG_1
        for i in range(1, 11):
            cell_address = "B" + str(i + 2)
            shape_name = "Question" + str(i)
            self._write(sheet_name, cell_address, SLIDE["KD_CHUNG_1"], shape_name)
        # KD_RIENG_1
        for i in range(1, 6):
            cell_address = "B" + str(i + 14)
            shape_name = "Question" + str(i)
            self._write(sheet_name, cell_address, SLIDE["KD_RIENG_1"], shape_name)
        # KD_RIENG_2
        for i in range(1, 6):
            cell_address = "B" + str(i + 21)
            shape_name = "Question" + str(i)
            self._write(sheet_name, cell_address, SLIDE["KD_RIENG_2"], shape_name)
        # KD_RIENG_3
        for i in range(1, 6):
            cell_address = "B" + str(i + 28)
            shape_name = "Question" + str(i)
            self._write(sheet_name, cell_address, SLIDE["KD_RIENG_3"], shape_name)
        # KD_RIENG_4
        for i in range(1, 6):
            cell_address = "B" + str(i + 35)
            shape_name = "Question" + str(i)
            self._write(sheet_name, cell_address, SLIDE["KD_RIENG_4"], shape_name)
        # KD_CHUNG_2
        for i in range(1, 11):
            cell_address = "B" + str(i + 42)
            shape_name = "Question" + str(i)
            self._write(sheet_name, cell_address, SLIDE["KD_CHUNG_2"], shape_name)
        print("De KHOI DONG da duoc load xong!")
    
    # VD Player 1
    def _load_vd_player_1(self, sheet_name="VD"):
        # NSHV
        for i in range(1, 4):
            start_index = 2
            cell_address = "B" + str(i + start_index)
            self._write(sheet_name, cell_address, SLIDE["VD1_NSHV"], f"Question{10 * i}Points")
            self._write(sheet_name, cell_address, SLIDE["VD1_CDTL"], f"Question{10 * i}Points")
            cell_address = "B" + str(i + start_index + 3)
            self._write(sheet_name, cell_address, SLIDE["VD1_NSHV"] + 1, f"Question{10 * i}Points")
            self._write(sheet_name, cell_address, SLIDE["VD1_CDTL"] + 1, f"Question{10 * i}Points")
            cell_address = "B" + str(i + start_index + 6)
            self._write(sheet_name, cell_address, SLIDE["VD1_NSHV"] + 2, f"Question{10 * i}Points")
            self._write(sheet_name, cell_address, SLIDE["VD1_CDTL"] + 2, f"Question{10 * i}Points")

        # CDND
        self._write(sheet_name, "B14", SLIDE["VD1_CDND"], "Question60Points")
        self._write(sheet_name, "B14", SLIDE["VD1_CDND"], "Question70Points")
        self._write(sheet_name, "B15", SLIDE["VD1_CDND"], "Question80Points")
        self._write(sheet_name, "B15", SLIDE["VD1_CDND"], "Question90Points")

    # VD Player 2
    def _load_vd_player_2(self, sheet_name="VD"):
        # NSHV
        for i in range(1, 4):
            start_index = 17
            cell_address = "B" + str(i + start_index)
            self._write(sheet_name, cell_address, SLIDE["VD2_NSHV"], f"Question{10 * i}Points")
            self._write(sheet_name, cell_address, SLIDE["VD2_CDTL"], f"Question{10 * i}Points")
            cell_address = "B" + str(i + start_index + 3)
            self._write(sheet_name, cell_address, SLIDE["VD2_NSHV"] + 1, f"Question{10 * i}Points")
            self._write(sheet_name, cell_address, SLIDE["VD2_CDTL"] + 1, f"Question{10 * i}Points")
            cell_address = "B" + str(i + start_index + 6)
            self._write(sheet_name, cell_address, SLIDE["VD2_NSHV"] + 2, f"Question{10 * i}Points")
            self._write(sheet_name, cell_address, SLIDE["VD2_CDTL"] + 2, f"Question{10 * i}Points")

        # CDND
        self._write(sheet_name, "B29", SLIDE["VD2_CDND"], "Question60Points")
        self._write(sheet_name, "B29", SLIDE["VD2_CDND"], "Question70Points")
        self._write(sheet_name, "B30", SLIDE["VD2_CDND"], "Question80Points")
        self._write(sheet_name, "B30", SLIDE["VD2_CDND"], "Question90Points")

    # VD Player 3
    def _load_vd_player_3(self, sheet_name="VD"):
        # NSHV
        for i in range(1, 4):
            start_index = 32
            cell_address = "B" + str(i + start_index)
            self._write(sheet_name, cell_address, SLIDE["VD3_NSHV"], f"Question{10 * i}Points")
            self._write(sheet_name, cell_address, SLIDE["VD3_CDTL"], f"Question{10 * i}Points")
            cell_address = "B" + str(i + start_index + 3)
            self._write(sheet_name, cell_address, SLIDE["VD3_NSHV"] + 1, f"Question{10 * i}Points")
            self._write(sheet_name, cell_address, SLIDE["VD3_CDTL"] + 1, f"Question{10 * i}Points")
            cell_address = "B" + str(i + start_index + 6)
            self._write(sheet_name, cell_address, SLIDE["VD3_NSHV"] + 2, f"Question{10 * i}Points")
            self._write(sheet_name, cell_address, SLIDE["VD3_CDTL"] + 2, f"Question{10 * i}Points")

        # CDND
        self._write(sheet_name, "B44", SLIDE["VD3_CDND"], "Question60Points")
        self._write(sheet_name, "B44", SLIDE["VD3_CDND"], "Question70Points")
        self._write(sheet_name, "B45", SLIDE["VD3_CDND"], "Question80Points")
        self._write(sheet_name, "B45", SLIDE["VD3_CDND"], "Question90Points")
    
    # VD Player 4
    def _load_vd_player_4(self, sheet_name="VD"):
        # NSHV
        for i in range(1, 4):
            start_index = 47
            cell_address = "B" + str(i + start_index)
            self._write(sheet_name, cell_address, SLIDE["VD4_NSHV"], f"Question{10 * i}Points")
            self._write(sheet_name, cell_address, SLIDE["VD4_CDTL"], f"Question{10 * i}Points")
            cell_address = "B" + str(i + start_index + 3)
            self._write(sheet_name, cell_address, SLIDE["VD4_NSHV"] + 1, f"Question{10 * i}Points")
            self._write(sheet_name, cell_address, SLIDE["VD4_CDTL"] + 1, f"Question{10 * i}Points")
            cell_address = "B" + str(i + start_index + 6)
            self._write(sheet_name, cell_address, SLIDE["VD4_NSHV"] + 2, f"Question{10 * i}Points")
            self._write(sheet_name, cell_address, SLIDE["VD4_CDTL"] + 2, f"Question{10 * i}Points")

        # CDND
        self._write(sheet_name, "B59", SLIDE["VD4_CDND"], "Question60Points")
        self._write(sheet_name, "B59", SLIDE["VD4_CDND"], "Question70Points")
        self._write(sheet_name, "B60", SLIDE["VD4_CDND"], "Question80Points")
        self._write(sheet_name, "B60", SLIDE["VD4_CDND"], "Question90Points")

    def load_vcnv(self):
        sheet_name = "VCNV"
        # Cau hoi hang ngang
        for i in range(1, 9):
            cell_address = "B" + str(i + 1)
            shape_name = "Question" + str(i)
            self._write(sheet_name, cell_address, SLIDE["VCNV"], shape_name)
        # Do dai hang ngang
        for i in range(1, 9):
            cell_address = "C" + str(i + 1)
            shape_name = "Clue" + str(i)
            self._write(sheet_name, cell_address, SLIDE["VCNV"], shape_name)
        # Dap an hang ngang
        for i in range(1, 9):
            cell_address = "D" + str(i + 1)
            shape_name = "Answer" + str(i)
            self._write(sheet_name, cell_address, SLIDE["VCNV"], shape_name)
        # Do dai CNV
        self._write(sheet_name, "A1", SLIDE["VCNV"], "CNVTitle")
        # Dap an CNV
        self._write(sheet_name, "B1", SLIDE["VCNV"], "DapAnCNV")
        print("De VUOT CHUONG NGAI VAT da duoc load xong!")

    def load_tt(self):
        sheet_name = "TT_HS"
        shape_name = "Question"
        for i in range(1, 6):
            cell_address = "B" + str(i + 2)
            self._write(sheet_name, cell_address, SLIDE[f"TT{i}"], shape_name)
            self._write(sheet_name, cell_address, SLIDE[f"TT{i}"] - 1, shape_name)
        print("De TANG TOC da duoc load xong!")

    def load_hs(self):
        sheet_name = "TT_HS"
        # Mat ma
        shape_name = "PhoneNumber"
        cell_address = "A11"
        self._write(sheet_name, cell_address, SLIDE["HS"], shape_name)
        # Cau hoi
        shape_name = "Question"
        cell_address = "B11"
        self._write(sheet_name, cell_address, SLIDE["HS"], shape_name)
        # Dap an
        shape_name = "Answer"
        cell_address = "C11"
        self._write(sheet_name, cell_address, SLIDE["HS"], shape_name)
        print("De HOI SUC da duoc load xong!")

    def load_vd(self):
        sheet_name = "VD"
        self._load_vd_player_1(sheet_name)
        self._load_vd_player_2(sheet_name)
        self._load_vd_player_3(sheet_name)
        self._load_vd_player_4(sheet_name)
        print("De VE DICH da duoc load xong!")

    def load_chp(self):
        sheet_name = "CHP"
        for i in range(1, 6):
            shape_name = "Question" + str(i)
            cell_address = "B" + str(i + 1)
            self._write(sheet_name, cell_address, SLIDE["CHP"], shape_name)
        print("De CAU HOI PHU da duoc load xong!")

    def load(self):
        self.load_kd()
        self.load_vcnv()
        self.load_tt()
        self.load_hs()
        self.load_vd()
        self.load_chp()
        self.save()
    
    def save(self):
        # Save and close the presentation
        self.presentation.Save()
        self.presentation.Close()

        # Close the workbook
        self.workbook.Close(SaveChanges=False)
        
        # Quit the applications
        self.excel_app.Quit()
        self.ppt_app.Quit()

if __name__ == "__main__":
    loader = Loader()
    loader.load()
    