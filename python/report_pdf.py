from collections import defaultdict
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.flowables import Flowable
from reportlab.platypus import Image, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from datetime import datetime
import numpy as np
import os

# The code cannot be finished without kaiwen's help !
# src code: https://github.com/MASILab/thorax_bcomp_pipeline_docker_version/blob/7289b40756804b62a9f458cb1c2f24963db4b944/src/Utils/pdf_report.py

class verticalTextLeft(Flowable):
    """
    Rotates a text in a table cell.
    """

    def __init__(self, text, font_name, font_size, y_offset):
        Flowable.__init__(self)
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.y_offset = y_offset

    def draw(self):
        my_canvas = self.canv
        my_canvas.setFont(self.font_name, self.font_size)
        str_width = my_canvas.stringWidth(self.text, self.font_name, self.font_size)
        my_canvas.translate(-0.3 * self.font_size, -0.5 * str_width + self.y_offset)
        my_canvas.rotate(90)
        my_canvas.drawString(0, 0, self.text)

    def wrap(self, aW, aH):
        canv = self.canv
        fn, fs = canv._fontname, canv._fontsize
        # fn = self.font_name
        # fs = self.font_size
        return canv._leading, canv.stringWidth(self.text, fn, fs)


class TextTop(Flowable):
    """
    Rotates a text in a table cell.
    """

    def __init__(self, text, font_name, font_size, x_offset, y_offset):
        Flowable.__init__(self)
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.x_offset = x_offset
        self.y_offset = y_offset

    def draw(self):
        my_canvas = self.canv
        my_canvas.setFont(self.font_name, self.font_size)
        str_width = my_canvas.stringWidth(self.text, self.font_name, self.font_size)
        my_canvas.translate(self.x_offset - 0.5 * str_width, self.y_offset + 0.2 * self.font_size)
        # my_canvas.translate(-0.2 * self.font_size, -0.5 * str_width + self.y_offset)
        # my_canvas.rotate(90)
        my_canvas.drawString(0, 0, self.text)

    def wrap(self, aW, aH):
        canv = self.canv
        fn, fs = canv._fontname, canv._fontsize
        # fn = self.font_name
        # fs = self.font_size
        return canv._leading, canv.stringWidth(self.text, fn, fs)


class TextTopSubtitle(Flowable):
    """
    Rotates a text in a table cell.
    """

    def __init__(self, text, font_name, font_size, x_offset, y_offset):
        Flowable.__init__(self)
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.x_offset = x_offset
        self.y_offset = y_offset

    def draw(self):
        my_canvas = self.canv
        my_canvas.setFont(self.font_name, self.font_size)
        # my_canvas.translate(0, self.y_offset + 0.2 * self.font_size)
        my_canvas.translate(self.x_offset, self.y_offset + 0.3 * self.font_size)
        my_canvas.drawRightString(0, 0, self.text)

    def wrap(self, aW, aH):
        canv = self.canv
        fn, fs = canv._fontname, canv._fontsize
        # fn = self.font_name
        # fs = self.font_size
        return canv._leading, canv.stringWidth(self.text, fn, fs)


class TextMainMiddle(Flowable):
    """
    Rotates a text in a table cell.
    """

    def __init__(self, text, font_name, font_size, x_offset, y_offset):
        Flowable.__init__(self)
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.x_offset = x_offset
        self.y_offset = y_offset

    def draw(self):
        my_canvas = self.canv
        my_canvas.setFont(self.font_name, self.font_size)
        # my_canvas.translate(0, self.y_offset + 0.2 * self.font_size)
        my_canvas.translate(self.x_offset, self.y_offset)
        my_canvas.drawCentredString(0, 0, self.text)

    def wrap(self, aW, aH):
        canv = self.canv
        fn, fs = canv._fontname, canv._fontsize
        # fn = self.font_name
        # fs = self.font_size
        return canv._leading, canv.stringWidth(self.text, fn, fs)


class MuscleReportGenerator:
    def __init__(
            self,
            case_info_dict
    ):
        """
        Required contents for case_info_dict:
        + result:
            + gracilis intensity mean/std, area (mm2) 
            + hamstring intensity mean/std, area (mm2)
            + quadriceps femoris intensity mean/std, area(mm2)
            + satourious intensity mean/std, area(mm2)
        + snapshot:
            + original scale image and segmentation image
        :param case_info_dict:
        """
        self.case_info_dict = case_info_dict
        self.masi_logo = os.path.join('/MATERIAL','masi.png')

        font_normal_ttf = os.path.join('/MATERIAL', 'helvetica.ttf')
        font_bold_ttf = os.path.join('/MATERIAL', 'helvetica-bold.ttf')
        pdfmetrics.registerFont(TTFont('CustomFont', font_normal_ttf))
        pdfmetrics.registerFont(TTFont('CustomFontBold', font_bold_ttf))

    def draw_report(self, out_pdf):
        width, height = A4
        margin_size = 0.17 * inch 
        text_margin_size = 0.17 * inch


        block_snapshot_height = 0.25 * height
        block_result_height = 0.15 * height
        block_info_height = 0.6 * height - block_snapshot_height - block_result_height - text_margin_size - 4 * margin_size

        height = height * 0.6

        title_font_size = 17
        title_font_name = 'CustomFont'

        subtitle_font_size = 15
        subtitle_font_name = 'CustomFontBold'

        main_text_font_size = 12
        main_text_font_name = 'CustomFont'

        result_text_font_size = 14
        result_text_font_name = 'CustomFont'

        info_text_font_size = 12
        info_text_font_name = 'CustomFont'

        line_stroke = 1

        # Configuration for the snapshot block
        config_snapshot = {
            'masi_logo_height': 0.6 * block_snapshot_height,
            'masi_logo_wh_ratio': 580. / 616.,
            'txt_margin': 0.2 * inch,
            'border_margin': 0.2 * inch,
            'img_wh_ratio': 2}

        # report_filename = 'sefov_report.pdf'
        report = canvas.Canvas(
            out_pdf,
            pagesize=(width, height))

        # --- Add the block from bottom up

        # Step.1 The "info" block.
        # block_width = width - 2 * margin_size - text_margin_size
        horizontal_margin = 2 * (margin_size + text_margin_size)
        block_width = width - 2 * horizontal_margin
        report.translate(
            # horizontal_margin + text_margin_size,
            horizontal_margin,
            margin_size)
        # Add text on the left
        info_txt_flowable = verticalTextLeft('INFO', title_font_name, title_font_size, 0.5 * block_info_height)
        info_txt_flowable.drawOn(report, 0, 0)
        # Add block boundary
        report.rect(
            0, 0,
            block_width,
            block_info_height,
            stroke=line_stroke)

        # Fill text into the info block
        def draw_text(text_str, x, y):
            text_obj = report.beginText(x, y)
            text_obj.setFont(
                info_text_font_name,
                info_text_font_size)
            for line_str in text_str.splitlines(False):
                text_obj.textLine(line_str.rstrip())
            report.drawText(text_obj)
        text_pdf_report_file = f'PDF Report: {os.path.basename(out_pdf)}'
        text_citation = 'Citation: Qi Yang et al., "Transferring Inter-modality Information for Thigh CT \nSlice with Self Training" (Submitted to IEEE Transaction Biomedical Engineering)'
        text_contact = 'Contact:qi.yang@vanderbilt.edu'
        text_time_str = datetime.now().ctime()
        text_version_str = 'Version: v1.0.0 (October 19, 2022)'

        y_anchor = block_info_height - 1.5 * margin_size
        draw_text(text_pdf_report_file, margin_size, y_anchor)
        y_anchor = y_anchor - 1.5 * info_text_font_size
        draw_text(text_citation, margin_size, y_anchor)
        y_anchor = y_anchor - 3 * info_text_font_size
        draw_text(text_contact, margin_size, y_anchor)

        draw_text(text_time_str, margin_size, 0.5 * margin_size)
        draw_text(text_version_str, block_width - 17 * info_text_font_size, 0.5 * margin_size)

        # Step.2 The "Result" block.
        report.translate(0, margin_size + block_info_height)
        # Add text on the left
        info_txt_flowable = verticalTextLeft('RESULT', title_font_name, title_font_size, 0.5 * block_result_height)
        info_txt_flowable.drawOn(report, 0, 0)
        # Add block frame
        report.rect(
            0, 0,
            block_width,
            block_result_height,
            stroke=line_stroke)

        
        file_name = self.case_info_dict['file_name']
        result_text = f'Image file: {file_name}'
        result_text_obj = report.beginText(margin_size, block_result_height - 1.5 * margin_size)
        result_text_obj.setFont(
            result_text_font_name,
            result_text_font_size
        )
        for line in result_text.splitlines(False):
            result_text_obj.textLine(line.rstrip())
        report.drawText(result_text_obj)

        # Add the muscle table at three levels respectively.
        muscle_table_width_ratio = 1
        muscle_table_config = {
            'height': block_result_height - 4 * margin_size,
            'width': (block_width - 3 * margin_size) * muscle_table_width_ratio
        }
        mean_intensity_row_str_items = ['Mean Intensity']
        mean_intensity_list = self.case_info_dict['result']['mean_intensity_list']
        for mean_intensity in mean_intensity_list:
            if np.isnan(mean_intensity):
                mean_intensity_row_str_items += ['']
            else: 
                mean_intensity_row_str_items += [f'{mean_intensity:.4f}']

        intensity_std_row_str_items = ['Intensity std']
        intensity_std_list = self.case_info_dict['result']['std_list']

        for intensity_std in intensity_std_list:
            if np.isnan(intensity_std):
                intensity_std_row_str_items += ['']
            else: 
                intensity_std_row_str_items += [f'{intensity_std:.4f}']

        area_row_str_items = ['area (mm^2)']
        area_list = self.case_info_dict['result']['area_list']

        for area in area_list:
            if np.isnan(area):
                area_row_str_items += ['']
            else: 
                area_row_str_items += [f'{area:.4f}']


        muscle_table_data = [
            ['', 'Satorious', 'Hamstring', 'Quadriceps','Gracilis'],
            mean_intensity_row_str_items,
            intensity_std_row_str_items,
            area_row_str_items
        ]
        muscle_table_first_column_width = 100
        muscle_table_rest_column_width = (muscle_table_config['width'] - muscle_table_first_column_width) / 4
        muscle_table = Table(
            muscle_table_data,
            [muscle_table_first_column_width] + 4 * [muscle_table_rest_column_width],
            4 * [muscle_table_config['height'] / 4.])
        muscle_table.setStyle(
            TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, -1), result_text_font_size),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black)
            ])
        )
        muscle_table.wrap(muscle_table_config['width'], muscle_table_config['height'])
        muscle_table.drawOn(report, margin_size, 0.5 * margin_size)

        # Step.3 The "Snapshot" block
        report.translate(0, margin_size + block_result_height)
        # Add text to the left
        info_txt_flowable = verticalTextLeft('SNAPSHOT', title_font_name, title_font_size, 0.5 * block_snapshot_height)
        info_txt_flowable.drawOn(report, 0, 0)
        # Add block frame
        report.rect(
            0, 0,
            block_width,
            block_snapshot_height,
            stroke=line_stroke
        )

        # Add the title
        title_txt_flowable = TextTop(
            'Muscle Group Segmentaton Report for CT Slice Thigh',
            title_font_name,
            title_font_size,
            0.5 * block_width,
            block_snapshot_height
        )
        title_txt_flowable.drawOn(report, 0, 0)

        # Add the three figures
        config_snapshot['masi_logo_width'] = config_snapshot['masi_logo_height'] * config_snapshot['masi_logo_wh_ratio']
        config_snapshot['img_height'] = \
            config_snapshot['masi_logo_height'] + \
            2 * config_snapshot['txt_margin']
        config_snapshot['img_width'] = \
            config_snapshot['img_height'] * \
            config_snapshot['img_wh_ratio']
        config_snapshot['fov_seg_height'] = config_snapshot['border_margin']
      

        # The masi logo
        masi_logo_flowable = Image(
            self.masi_logo,
            width=config_snapshot['masi_logo_width'],
            height=config_snapshot['masi_logo_height']
        )
        masi_logo_flowable.drawOn(
            report,
            config_snapshot['border_margin'],
            config_snapshot['border_margin'])
        

        # The vert_pred image
        vert_pred_flowable = Image(
            self.case_info_dict['snapshot']['img_pred'],
            width=config_snapshot['img_width'],
            height=config_snapshot['img_height']
        )
        vert_pred_flowable.drawOn(
            report,
            block_width - (config_snapshot['border_margin'] + config_snapshot['img_width']),
            config_snapshot['border_margin']
        )
        vert_pred_text = TextTopSubtitle(
            "rescale CT image and segmentation",
            subtitle_font_name,
            subtitle_font_size,
            block_width - config_snapshot['border_margin'],
            block_snapshot_height - config_snapshot['border_margin'] - config_snapshot['txt_margin']
        )
        vert_pred_text.drawOn(report, 0, 0)

        report.showPage()
        report.save()

# if __name__ == '__main__':
#     info_dict = {}
#     info_dict['file_name'] = 'test.nii.gz'
#     info_dict['result'] = {}
#     info_dict['result']['intensity_list'] = [np.nan,np.nan,np.nan,np.nan] 
#     info_dict['result']['std_list'] = [np.nan,0.421,0.412,0.131,]
#     info_dict['result']['area_list'] = [123.421,24901.2,582.4,18291.1243]
#     info_dict['snapshot'] = {}
#     info_dict['snapshot']['img_pred'] = '/nfs/masi/yangq6/BLSA_leg/paper/2022_TBME/qua_fig/proposed_vis_latest/BLSA_7972-03-2011-04-05_CT_NIA_BLSA_5_right_res.png'
    

#     gen = MuscleReportGenerator(info_dict)
#     gen.draw_report('./test.pdf')