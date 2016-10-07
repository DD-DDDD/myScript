library(ggplot2)
library(plotly)

data_mining<-read.csv("C:/Users/ricaito/Desktop/test/shujuwajue_job.csv")
data_mining<-data_mining[(!duplicated(data_mining)),]
#对数据集进行重复值的剔除
local<-ggplot(data = data_mining,mapping = aes(x = city))+geom_bar()
local<-ggplotly(local)
#各个城市对数据挖掘人员的需求
company_type<-ggplot(data = data_mining,mapping = aes(x = financeStage))+geom_bar()
company_type<-ggplotly(company_type)
#什么类型的公司对数据挖掘的人员的需求
salary<-ggplot(data = data_mining,mapping = aes(x = city,y = salary))+geom_point(position = "jitter")
salary<-ggplotly(salary)
#不同地区的工资的散点分布
degree<-ggplot(data = data_mining,mapping = aes(x = factor(1),fill = factor(education)))+geom_bar(width = 1)+coord_polar(theta = "y")
#数据挖掘人员的学历需求
work_experience<-ggplot(data = data_mining,mapping = aes(x = factor(1),fill = factor(workYear)))+geom_bar(width = 1)+coord_polar(theta = "y")
#对数据挖掘人员的工作经验的需求


