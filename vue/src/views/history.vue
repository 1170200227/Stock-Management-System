<template>
    <div height="840px" width="800px">
        <el-header style="background-color: #ffffff;margin-left: 25px;margin-right: 25px;border-bottom: 1px solid rgb(28, 202, 213);">
            <el-select v-model="value1" placeholder="Please select stock code" style="">
                <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                </el-option>
            </el-select>
            <el-date-picker style="margin-left:  14px"
                    v-model="value2"
                    type="date"
                    placeholder="Please select start date">
            </el-date-picker>
            <el-date-picker style="margin-left:  14px"
                    v-model="value3"
                    type="date"
                    placeholder="Please select end date">
            </el-date-picker>
            <el-button type="primary" @click="query(value1, value2, value3)" style="margin-left: 14px">QUERY</el-button>
        </el-header>

        <div  ref="bar_dv"  style="width:96%;height: 600px; margin-left: 25px;margin-top: 20px"></div>
    </div>

</template>

<script>
    import echarts from 'echarts'
    export default {
        name: "History",
        data() {
            return {
                myChart:null,
				upColor: '#ec0000',
				upBorderColor: '#8A0000',
				downColor: '#00da3c',
				downBorderColor: '#008F28',
                options:[
                	{
                		value: '000001',
                		label: '000001'
                	},
                	{
                		value: '000002',
                		label: '000002'
                	},
                	{
                		value: '000003',
                		label: '000003'
                	},
                	{
                		value: '000004',
                		label: '000004'
                	},
                	{
                		value: '000005',
                		label: '000005'
                	},
                	{
                		value: '000006',
                		label: '000006'
                	}
                ],
                value1:null,
                value2:null,
                value3:null,
				categoryData: [],
				values: []
            }
        },
        created() {
            
        },
        methods: {
			calculateMA(dayCount) {
			  var result = [];
			  for (var i = 0, len = this.values.length; i < len; i++) {
			    if (i < dayCount) {
			      result.push('-');
			      continue;
			    }
			    var sum = 0;
			    for (var j = 0; j < dayCount; j++) {
			      sum += +this.values[i - j][1];
			    }
			    result.push(sum / dayCount);
			  }
			  return result;
			},
			getcharts() {
				this.myChart = echarts.init(this.$refs.bar_dv);
				let option = {
					title: {
						text: 'Candlestick Chart',
						left: 0
					},
					tooltip: {
						trigger: 'axis',
						axisPointer: {
							type: 'cross'
						}
					},
					legend: {
						data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30']
					},
					grid: {
						left: '10%',
						right: '10%',
						bottom: '15%'
					},
					xAxis: {
						type: 'category',
						data: this.categoryData,
						boundaryGap: false,
						axisLine: { onZero: false },
						splitLine: { show: false },
						min: 'dataMin',
						max: 'dataMax'
					},
					yAxis: {
						scale: true,
						splitArea: {
							show: true
						}
					},
					dataZoom: [
						{
							type: 'inside',
							start: 50,
							end: 100
						},
						{
							show: true,
							type: 'slider',
							top: '90%',
							start: 50,
							end: 100
						}
					],
					series: [
						{
							name: '日K',
							type: 'candlestick',
							data: this.values,
							itemStyle: {
							color: this.upColor,
							color0: this.downColor,
							borderColor: this.upBorderColor,
							borderColor0: this.downBorderColor
						},
						markPoint: {
							label: {
								formatter: function (param) {
									return param != null ? Math.round(param.value) + '' : '';
								}
							},
							data: [
								{
									name: 'Mark',
									coord: ['2013/5/31', 2300],
									value: 2300,
									itemStyle: {
										color: 'rgb(41,60,85)'
									}
								},
								{
									name: 'highest value',
									type: 'max',
									valueDim: 'highest'
								},
								{
									name: 'lowest value',
									type: 'min',
									valueDim: 'lowest'
								},
								{
									name: 'average value on close',
									type: 'average',
									valueDim: 'close'
								}
							],
							tooltip: {
								formatter: function (param) {
									return param.name + '<br>' + (param.data.coord || '');
								}
							}
						},
						markLine: {
							symbol: ['none', 'none'],
							data: [
							  [
								{
								  name: 'from lowest to highest',
								  type: 'min',
								  valueDim: 'lowest',
								  symbol: 'circle',
								  symbolSize: 10,
								  label: {
									show: false
								  },
								  emphasis: {
									label: {
									  show: false
									}
								  }
								},
								{
								  type: 'max',
								  valueDim: 'highest',
								  symbol: 'circle',
								  symbolSize: 10,
								  label: {
									show: false
								  },
								  emphasis: {
									label: {
									  show: false
									}
								  }
								}
							  ],
							  {
								name: 'min line on close',
								type: 'min',
								valueDim: 'close'
							  },
							  {
								name: 'max line on close',
								type: 'max',
								valueDim: 'close'
							  }
							]
						  }
						},
						{
						  name: 'MA5',
						  type: 'line',
						  data: this.calculateMA(5),
						  smooth: true,
						  lineStyle: {
							opacity: 0.5
						  }
						},
						{
						  name: 'MA10',
						  type: 'line',
						  data: this.calculateMA(10),
						  smooth: true,
						  lineStyle: {
							opacity: 0.5
						  }
						},
						{
						  name: 'MA20',
						  type: 'line',
						  data: this.calculateMA(20),
						  smooth: true,
						  lineStyle: {
							opacity: 0.5
						  }
						},
						{
						  name: 'MA30',
						  type: 'line',
						  data: this.calculateMA(30),
						  smooth: true,
						  lineStyle: {
							opacity: 0.5
						  }
						}
					  ]
					};
				this.myChart.setOption(option);	
			},
			query(value1, value2, value3) {
				var month = this.value2.getMonth() + 1;
				if(month < 10)
				    month = "0"+month;
				var Date = this.value2.getDate();
				if(Date < 10)
				    Date = "0" + Date;
				var start_date = this.value2.getFullYear() + "" + month + "" + Date
				month = this.value3.getMonth() + 1;
				if(month < 10)
				    month = "0"+month;
				Date = this.value3.getDate();
				if(Date < 10)
				    Date = "0" + Date;
				var end_date = this.value3.getFullYear() + "" + month + "" + Date
				console.log(value1)
				console.log(start_date)
				console.log(end_date)
				if (value1 != null && start_date != null && end_date != null) {
					var url = '/api/history/?code=' + value1 + '&start_date=' + start_date + '&end_date=' + end_date;
					const _this = this;
					axios.get(url).then(function(data){
						if (data.data != null && data.data != "") {
							_this.categoryData = [];
							_this.values = [];
							for (var i = 0; i < data.data.length; i++) {
								_this.categoryData.push([data.data[i].日期]);
								_this.values.push([data.data[i].开盘, data.data[i].收盘, data.data[i].最低, data.data[i].最高]);
							}
						}
					})
				}
				setTimeout(() =>{
				    this.getcharts();
				}, 2000);
			}
        }
    }
</script>

<style scoped>

</style>