import React from 'react';
import Highcharts from "highcharts/highmaps";
import HighchartsReact from "highcharts-react-official";
import ua_data from "../../ua-topo.json";
import ArticleService from "../../API/ArticleService";
import {DEFAULT_LIMIT} from "../../constants";


const Map = ({totalArticles, setSelectedRegion, setArticles, timeConfig, setRequestOffset}) => {
    const options = {
        title: {
            text: ''
        },
        tooltip: {
            enabled: false
        },
        chart: {
            map: ua_data,
            title:{
                text:''
            },
        },
        plotOptions:{
            series:{
                point:{
                    events:{
                        click: async function(){
                            setSelectedRegion(this.num);
                            setRequestOffset(0);
                            if (!this.numArticles) {return}
                            let newArticleData = await ArticleService.getArticlesByRegion(
                                timeConfig.fromTime,
                                timeConfig.toTime,
                                this.num,
                                DEFAULT_LIMIT,
                                0
                                )
                            setArticles(newArticleData)
                        }
                    }
                }
            }
        },
        series: [{
                name: '',
                showInLegend: false,
                nullColor: '#F3F4F8',
                borderColor: '#232360',
                borderWidth: 2
            },
            {
                name: '',
                showInLegend: false,
                dataLabels: {
                    enabled: true,
                    formatter: function () {
                        let numArticles;

                        if (!this.point.numArticles) {
                            numArticles = 'No data';
                        } else {
                            numArticles = this.point.numArticles
                        }
                        return '<span> (' + numArticles + ') ' + this.point.name + '</span>'
                    }
                },
                type: 'mappoint',
                color: Highcharts.getOptions().colors[1],
                data: totalArticles,
                marker: {
                    radius: 10,
                    fillColor: '#5051F9',
                    lineWidth: 2,
                    lineColor: "#232360"
                },

            }
            ],

        mapNavigation: {
            enabled: true,
            buttonOptions: {
                verticalAlign: 'bottom'
            }
        },
    }

    return (
        <div>
            <HighchartsReact
                highcharts={Highcharts}
                constructorType={'mapChart'}
                options={options}/>
        </div>
    );
};

export default Map;