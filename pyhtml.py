

class HTML:
    def __init__(self):
        self.MailHTML= """
            <!DOCTYPE html>
            <html>
            <link href="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
            <script src="https://cdn.bootcss.com/bootstrap/3.3.7/css/bootstrap-theme.min.css"></script>
            <script src="https://cdn.bootcss.com/jquery/2.1.1/jquery.min.js"></script>
            <script src="https://cdn.bootcss.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
            <head>
                <meta charset="UTF-8">
                <title>weibo监控机器人每日报告</title>
                <h3>weibo监控机器人每日报告</h3>
                <p class='attribute'><strong>生成日期 : </strong> {date_time}</p>
                <div><text>这是截至邮件发送时，24小时内总热度排名前 30 的热搜情况，目前为测试阶段</text></div>
            </head>
            <body>
                <table class="table table-condensed">
                    <thead>
                      <tr>
                         <th>热搜</th>
                         <th>总热度</th>
                         <th>最近更新时间</th>
                         <th>详情</th>
                      </tr>
                    </thead>
                    <tbody>
                    {table_tr}
                    </tbody>
                </table>
                <h5><strong>报告由机器自动生成，共耗时 {sec} 秒</strong></h5>
            </body>
            </html>"""

        self.TABLE_TMPL = """
            <tr>
                <td>{title}</td>
                <td>{hot_sum}</td>
                <td>{update_time}</td>
                <td><a href="{href}">点击查看</td>
            </tr>"""