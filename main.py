"""
施工现场罚款系统 - 安卓APP
"""
import json
import os
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivy.utils import platform
from plyer import camera
from plyer import filechooser
from fpdf import FPDF
import io
import base64
import requests

class FineSystemApp(App):
    def build(self):
        self.title = "施工现场罚款系统"
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = Label(
            text='📸 施工现场罚款系统',
            font_size=24,
            size_hint_y=None,
            height=60
        )
        main_layout.add_widget(title)
        
        # 1. 图片选择区域
        img_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=250)
        
        img_label = Label(
            text='1️⃣ 拍照或选择图片',
            font_size=16,
            size_hint_y=None,
            height=40
        )
        img_layout.add_widget(img_label)
        
        self.image_preview = Image(
            source='',
            size_hint=(1, None),
            height=150,
            allow_stretch=True
        )
        img_layout.add_widget(self.image_preview)
        
        img_buttons = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        
        camera_btn = Button(
            text='📷 拍照',
            background_color=(0.4, 0.5, 0.9, 1)
        )
        camera_btn.bind(on_press=self.take_photo)
        img_buttons.add_widget(camera_btn)
        
        gallery_btn = Button(
            text='📁 选择图片',
            background_color=(0.4, 0.5, 0.9, 1)
        )
        gallery_btn.bind(on_press=self.choose_image)
        img_buttons.add_widget(gallery_btn)
        
        img_layout.add_widget(img_buttons)
        main_layout.add_widget(img_layout)
        
        # 2. 违规事项输入
        violation_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=150)
        
        violation_label = Label(
            text='2️⃣ 输入违规事项',
            font_size=16,
            size_hint_y=None,
            height=40
        )
        violation_layout.add_widget(violation_label)
        
        self.violation_input = TextInput(
            hint_text='请输入违规事项关键词（例如：未戴安全帽、未系安全带）',
            size_hint=(1, None),
            height=80,
            multiline=False
        )
        violation_layout.add_widget(self.violation_input)
        main_layout.add_widget(violation_layout)
        
        # 3. 罚款金额选择
        amount_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=180)
        
        amount_label = Label(
            text='3️⃣ 选择罚款金额',
            font_size=16,
            size_hint_y=None,
            height=40
        )
        amount_layout.add_widget(amount_label)
        
        # 金额按钮网格
        amounts_layout = GridLayout(cols=3, size_hint_y=None, height=120, spacing=10, padding=10)
        
        amounts = ['100', '200', '500', '1000', '2000', '5000']
        self.amount_buttons = {}
        
        for amount in amounts:
            btn = Button(
                text=f'¥{amount}',
                font_size=20,
                background_color=(0.9, 0.9, 0.9, 1)
            )
            btn.bind(on_press=lambda instance, a=amount: self.select_amount(a))
            amounts_layout.add_widget(btn)
            self.amount_buttons[amount] = btn
        
        amount_layout.add_widget(amounts_layout)
        main_layout.add_widget(amount_layout)
        
        # 4. 生成按钮
        self.generate_btn = Button(
            text='🤖 AI分析并生成罚款单',
            font_size=20,
            size_hint_y=None,
            height=60,
            background_color=(0.4, 0.5, 0.9, 1),
            disabled=True
        )
        self.generate_btn.bind(on_press=self.generate_fine)
        main_layout.add_widget(self.generate_btn)
        
        # 5. 导出按钮
        self.export_btn = Button(
            text='📤 导出PDF罚款单',
            font_size=18,
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.8, 0.4, 1),
            disabled=True
        )
        self.export_btn.bind(on_press=self.export_pdf)
        main_layout.add_widget(self.export_btn)
        
        # 6. 结果显示
        self.result_label = Label(
            text='',
            font_size=14,
            text_size=(None, None),
            halign='left',
            valign='top',
            size_hint=(1, 1),
            color=(0.2, 0.2, 0.2, 1)
        )
        main_layout.add_widget(self.result_label)
        
        # 初始化变量
        self.current_image = None
        self.selected_amount = None
        self.analysis_result = None
        self.history_file = 'fine_history.json'
        
        # 加载历史记录
        self.load_history()
        
        return main_layout
    
    def take_photo(self, instance):
        """拍照功能"""
        try:
            filepath = camera.take_picture(
                filename='temp_photo.jpg',
                on_complete=self.camera_callback
            )
        except Exception as e:
            self.show_popup('错误', f'拍照失败：{str(e)}')
    
    def camera_callback(self, filepath):
        """拍照回调"""
        if filepath and os.path.exists(filepath):
            self.current_image = filepath
            self.image_preview.source = filepath
            self.check_generate_button()
    
    def choose_image(self, instance):
        """选择图片功能"""
        try:
            filechooser.open_file(
                on_selection=self.file_selection_callback,
                path='/sdcard',
                multiple=False,
                filters=['*.jpg', '*.jpeg', '*.png']
            )
        except Exception as e:
            self.show_popup('错误', f'选择图片失败：{str(e)}')
    
    def file_selection_callback(self, selection):
        """文件选择回调"""
        if selection:
            self.current_image = selection[0]
            self.image_preview.source = selection[0]
            self.check_generate_button()
    
    def select_amount(self, instance, amount):
        """选择罚款金额"""
        self.selected_amount = amount
        
        # 更新按钮样式
        for amt, btn in self.amount_buttons.items():
            if amt == amount:
                btn.background_color = (0.4, 0.5, 0.9, 1)
            else:
                btn.background_color = (0.9, 0.9, 0.9, 1)
        
        self.check_generate_button()
    
    def check_generate_button(self):
        """检查生成按钮是否可用"""
        can_generate = self.current_image and self.selected_amount and self.violation_input.text.strip()
        self.generate_btn.disabled = not can_generate
    
    def generate_fine(self, instance):
        """生成罚款单"""
        violation = self.violation_input.text.strip()
        
        if not violation:
            self.show_popup('提示', '请输入违规事项关键词')
            return
        
        # 显示加载提示
        self.result_label.text = 'AI 正在分析中，请稍候...'
        self.generate_btn.disabled = True
        
        # 调用API
        self.call_qwen_api(self.current_image, self.selected_amount, violation)
    
    def call_qwen_api(self, image_path, amount, violation):
        """调用千问API"""
        # 读取图片并转为base64
        try:
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode()
        except Exception as e:
            self.show_popup('错误', f'读取图片失败：{str(e)}')
            self.generate_btn.disabled = False
            return
        
        # API配置
        API_URL = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation'
        API_KEY = 'sk-cd0c0e4340b74d5c8490cb634f08dbe2'
        
        prompt = f"""你是一个施工现场安全监督专家。请分析这张施工现场照片，针对以下违规事项进行详细说明：

违规事项：{violation}

要求：
1. 针对指定的违规事项进行详细分析
2. 说明违规的具体情况和危害
3. 针对该违规事项给出具体、可操作的整改意见
4. 返回JSON格式，包含：
   - violation: 违规事项（使用输入的关键词）
   - description: 违规说明（详细描述违规情况和危害）
   - suggestion: 整改意见（具体、可操作的整改措施）

罚款金额：{amount}元"""
        
        # 准备请求数据
        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'qwen-vl-max',
            'input': {
                'messages': [
                    {
                        'role': 'user',
                        'content': [
                            {
                                'image': image_data
                            },
                            {
                                'text': prompt
                            }
                        ]
                    }
                ]
            }
        }
        
        # 发送请求
        try:
            req = UrlRequest(
                API_URL,
                req_body=json.dumps(data),
                req_headers=headers,
                method='POST',
                on_success=lambda req, resp: self.on_api_success(req, resp),
                on_error=lambda req, resp: self.on_api_error(req, resp)
            )
        except Exception as e:
            self.show_popup('错误', f'API调用失败：{str(e)}')
            self.generate_btn.disabled = False
            self.result_label.text = ''
    
    def on_api_success(self, req, resp):
        """API成功回调"""
        try:
            result = json.loads(resp.decode('utf-8'))
            
            # 解析响应
            content = ''
            if 'output' in result and 'choices' in result['output']:
                message = result['output']['choices'][0]['message']
                if 'content' in message:
                    if isinstance(message['content'], list):
                        content = message['content'][0].get('text', '')
                    else:
                        content = message['content']
            
            # 解析JSON
            json_match = None
            import re
            match = re.search(r'\{[\s\S]*\}', content)
            if match:
                try:
                    json_match = json.loads(match.group())
                except:
                    pass
            
            if json_match:
                self.analysis_result = {
                    'violation': json_match.get('violation', violation),
                    'description': json_match.get('description', '照片显示施工现场情况'),
                    'suggestion': json_match.get('suggestion', '请根据实际情况确认整改意见'),
                    'amount': self.selected_amount,
                    'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'image': self.current_image
                }
                
                # 显示结果
                result_text = f"""✅ 分析完成！

📌 违规事项：{self.analysis_result['violation']}

💰 罚款金额：¥{self.analysis_result['amount']} 元

📝 违规说明：
{self.analysis_result['description']}

🔧 整改意见：
{self.analysis_result['suggestion']}

📅 记录时间：{self.analysis_result['time']}"""
                
                self.result_label.text = result_text
                self.export_btn.disabled = False
                
                # 保存到历史记录
                self.save_to_history(self.analysis_result)
                
            else:
                self.show_popup('提示', '无法解析API返回结果')
                self.generate_btn.disabled = False
                self.result_label.text = ''
                
        except Exception as e:
            self.show_popup('错误', f'解析响应失败：{str(e)}')
            self.generate_btn.disabled = False
            self.result_label.text = ''
    
    def on_api_error(self, req, resp):
        """API错误回调"""
        self.show_popup('错误', f'API调用失败，请检查网络连接')
        self.generate_btn.disabled = False
        self.result_label.text = ''
    
    def export_pdf(self, instance):
        """导出PDF"""
        if not self.analysis_result:
            self.show_popup('提示', '请先生成罚款单')
            return
        
        try:
            # 创建PDF
            pdf = FPDF()
            pdf.add_page()
            
            # 设置中文字体（使用默认字体，可能需要额外配置）
            pdf.set_font('Arial', '', 12)
            
            # 标题
            pdf.set_font_size(20)
            pdf.cell(0, 10, '施工现场罚款单', ln=True, align='C')
            pdf.ln(5)
            
            # 添加图片
            if os.path.exists(self.analysis_result['image']):
                pdf.image(self.analysis_result['image'], x=10, y=30, w=90)
            
            y_pos = 110
            
            # 违规事项
            pdf.set_font_size(14)
            pdf.set_fill_color(102, 126, 234)
            pdf.cell(0, 8, '📌 违规事项', ln=True, fill=True)
            pdf.ln(3)
            pdf.set_font_size(12)
            pdf.set_fill_color(248, 249, 250)
            pdf.multi_cell(0, 6, self.analysis_result['violation'], fill=True)
            pdf.ln(5)
            
            # 罚款金额
            y_pos = pdf.get_y()
            pdf.set_font_size(14)
            pdf.set_fill_color(231, 76, 60)
            pdf.cell(0, 8, '💰 罚款金额', ln=True, fill=True)
            pdf.ln(3)
            pdf.set_font_size(24)
            pdf.set_fill_color(255, 245, 245)
            pdf.cell(0, 15, f'¥{self.analysis_result["amount"]} 元', ln=True, align='C', fill=True)
            pdf.ln(5)
            
            # 违规说明
            pdf.set_font_size(14)
            pdf.set_fill_color(52, 152, 219)
            pdf.cell(0, 8, '📝 违规说明', ln=True, fill=True)
            pdf.ln(3)
            pdf.set_font_size(12)
            pdf.set_fill_color(248, 249, 250)
            pdf.multi_cell(0, 6, self.analysis_result['description'], fill=True)
            pdf.ln(5)
            
            # 整改意见
            pdf.set_font_size(14)
            pdf.set_fill_color(46, 204, 113)
            pdf.cell(0, 8, '🔧 整改意见', ln=True, fill=True)
            pdf.ln(3)
            pdf.set_font_size(12)
            pdf.set_fill_color(248, 249, 250)
            pdf.multi_cell(0, 6, self.analysis_result['suggestion'], fill=True)
            pdf.ln(5)
            
            # 记录时间
            pdf.set_font_size(14)
            pdf.set_fill_color(149, 165, 166)
            pdf.cell(0, 8, '📅 记录时间', ln=True, fill=True)
            pdf.ln(3)
            pdf.set_font_size(12)
            pdf.set_fill_color(250, 250, 250)
            pdf.cell(0, 6, self.analysis_result['time'], fill=True)
            pdf.ln(10)
            
            # 底部信息
            pdf.set_font_size(9)
            pdf.set_fill_color(0, 0, 0)
            pdf.cell(0, 5, '生成系统：施工现场罚款系统 | AI 分析：千问大模型', ln=True, fill=True)
            pdf.cell(0, 5, '此罚款单由AI辅助生成，最终以人工审核为准', ln=True, fill=True)
            
            # 保存PDF
            if platform == 'android':
                save_path = f'/sdcard/Download/罚款单_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
            else:
                save_path = f'罚款单_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
            
            pdf.output(save_path)
            
            self.show_popup('成功', f'PDF已保存到：\n{save_path}')
            
        except Exception as e:
            self.show_popup('错误', f'导出PDF失败：{str(e)}')
    
    def save_to_history(self, result):
        """保存到历史记录"""
        try:
            history = []
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            
            history.insert(0, result)
            
            # 只保留最近100条
            if len(history) > 100:
                history = history[:100]
            
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f'保存历史记录失败：{str(e)}')
    
    def load_history(self):
        """加载历史记录"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    print(f'加载了 {len(history)} 条历史记录')
        except Exception as e:
            print(f'加载历史记录失败：{str(e)}')
    
    def show_popup(self, title, message):
        """显示弹窗"""
        popup = Popup(
            title=title,
            content=Label(text=message, font_size=14, text_size=(300, None)),
            size_hint=(0.8, 0.4)
        )
        popup.open()

if __name__ == '__main__':
    FineSystemApp().run()
