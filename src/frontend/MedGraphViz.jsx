import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

const MedGraphViz = ({ data, vizType }) => {
  const [activeTab, setActiveTab] = useState('graph');

  // Format data for time series visualization
  const formatTimeSeriesData = (data) => {
    return data.map(item => ({
      date: new Date(item.date).toLocaleDateString(),
      value: item.value,
      category: item.category
    }));
  };

  // Format data for distribution visualization
  const formatDistributionData = (data) => {
    return Object.entries(data).map(([key, value]) => ({
      category: key,
      count: value
    }));
  };

  const renderTimeSeriesChart = (data) => (
    <div className="w-full h-96">
      <ResponsiveContainer>
        <LineChart data={formatTimeSeriesData(data)}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="value" stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );

  const renderDistributionChart = (data) => (
    <div className="w-full h-96">
      <ResponsiveContainer>
        <BarChart data={formatDistributionData(data)}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="category" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="count" fill="#82ca9d" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Medical Data Visualization</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue={activeTab} onValueChange={setActiveTab}>
          <TabsList>
            <TabsTrigger value="graph">Graph View</TabsTrigger>
            <TabsTrigger value="timeSeries">Time Series</TabsTrigger>
            <TabsTrigger value="distribution">Distribution</TabsTrigger>
          </TabsList>
          
          <TabsContent value="graph">
            {vizType === 'timeSeries' && renderTimeSeriesChart(data)}
          </TabsContent>
          
          <TabsContent value="timeSeries">
            {vizType === 'timeSeries' && renderTimeSeriesChart(data)}
          </TabsContent>
          
          <TabsContent value="distribution">
            {vizType === 'distribution' && renderDistributionChart(data)}
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
};

export default MedGraphViz;
