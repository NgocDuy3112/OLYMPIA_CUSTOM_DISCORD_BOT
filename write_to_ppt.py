import win32com.client as winclient

PPTApp = winclient.Dispatch("Powerpoint.Application")
PPTApp.visible = 1
PPTPresentation = PPTApp.ActivePresentation

ANSWER_SLIDE = {
    "VCNV": 18,
    "TT": 30,
    "HS": 34
}

def change_shape_content(presentation, slide_index, shape_name, new_content):
    try:
        # Access the specified slide (1-based index)
        slide = presentation.Slides(slide_index)

        # Find the shape by name
        shape = None
        for shp in slide.Shapes:
            if shp.Name == shape_name:
                shape = shp
                break

        if shape:
            print(f"Shape '{shape_name}' found: {shape.Name}")

            # Check if the shape has text
            if shape.HasTextFrame:
                shape.TextFrame.TextRange.Text = new_content
            else:
                print(f"Shape '{shape_name}' does not have a text frame.")
        else:
            print(f"Shape '{shape_name}' not found on slide {slide_index}.")

    except Exception as e:
        print(f"An error occurred: {e}")