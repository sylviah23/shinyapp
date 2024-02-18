import pandas as pd

from shiny import App, Inputs, Outputs, Session, render, ui
from shiny.types import FileInfo

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_file("files", "Choose images", multiple=True,accept="image/*"),
            ui.output_text("directions"),
            ui.output_ui("ui_action"),
        ),
        ui.panel_main(
            ui.output_table("orig_table_output"),
        ),
    ),
)

def server(input: Inputs, output: Outputs, session: Session):
    def data(): 
        """
        Returns a list, where each element of the list represents one of the input
        files and each element is itself a list containing the file name and its 
        spliced components
        """
        names=[]
        rows=[]
        for file in input.files():
            names.append(file.get("name"))

        for name in names:
            new=[]
            new.append(name)
            split=name.split('_')
            split[-1]=split[-1][:-4]
            for s in split:
                new.append(s)
            rows.append(new)
        return rows
    
    @output
    @render.text
    def directions():
        """
        Returns the directions/user guide for this shiny app
        """
        return "Upload the images that you would like to splice the file names of and a table will appear after the images finish uploading. If the table looks good, click on the 'Download' button that appears to download a csv of the table"

    @output
    @render.ui
    def ui_action():
        """
        Renders the ui for the "Download CSV" button after user input files 
        finish uploading
        """
        if (input.files() is None):
            return
        return ui.download_button("download", "Download CSV")

    @output
    @render.ui
    def orig_table_output():
        """
        Renders the ui for the table of data after user input files finish uploading
        """
        if input.files() is None:
            return "Please upload images"
        df_images = pd.DataFrame(data())
        return ui.HTML(df_images.to_html(classes="table table-striped"))
    
    @session.download(filename="data.csv")
    def download():
        """
        Users are able to download a csv of the table that appears after user
        input files finish uploading
        """
        df_images=pd.DataFrame(data())
        yield df_images.to_csv()

app = App(app_ui, server)