import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { DollarSign, TrendingUp, Users, Car, AlertTriangle, CheckCircle } from 'lucide-react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [profitability, setProfitability] = useState([]);
  const [expiringDocs, setExpiringDocs] = useState({ expiring_soon: [], expired: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const token = localStorage.getItem('token');
      const config = {
        headers: { Authorization: `Bearer ${token}` }
      };

      const [statsRes, profitRes, docsRes] = await Promise.all([
        axios.get(`${API_URL}/dashboard/stats`, config),
        axios.get(`${API_URL}/dashboard/vehicle-profitability`, config),
        axios.get(`${API_URL}/dashboard/expiring-documents`, config)
      ]);

      setStats(statsRes.data);
      setProfitability(profitRes.data.slice(0, 5));
      setExpiringDocs(docsRes.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Cargando...</div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Ingresos del Mes</p>
              <p className="text-2xl font-bold text-green-600">
                ${stats?.total_income?.toFixed(2) || '0.00'}
              </p>
            </div>
            <div className="bg-green-100 p-3 rounded-full">
              <DollarSign className="w-6 h-6 text-green-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Gastos del Mes</p>
              <p className="text-2xl font-bold text-red-600">
                ${stats?.total_expenses?.toFixed(2) || '0.00'}
              </p>
            </div>
            <div className="bg-red-100 p-3 rounded-full">
              <TrendingUp className="w-6 h-6 text-red-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Vehículos Activos</p>
              <p className="text-2xl font-bold text-blue-600">
                {stats?.active_vehicles || 0}/{stats?.total_vehicles || 0}
              </p>
            </div>
            <div className="bg-blue-100 p-3 rounded-full">
              <Car className="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Conductores Activos</p>
              <p className="text-2xl font-bold text-purple-600">
                {stats?.active_drivers || 0}
              </p>
            </div>
            <div className="bg-purple-100 p-3 rounded-full">
              <Users className="w-6 h-6 text-purple-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Profit and Alerts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Net Profit */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Balance Neto</h3>
          <div className={`text-4xl font-bold ${
            (stats?.net_profit || 0) >= 0 ? 'text-green-600' : 'text-red-600'
          }`}>
            ${stats?.net_profit?.toFixed(2) || '0.00'}
          </div>
          <p className="text-sm text-gray-500 mt-2">
            Período: {stats?.period?.month}/{stats?.period?.year}
          </p>
        </div>

        {/* Document Alerts */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Vencimientos de Documentos</h3>
          
          {expiringDocs.expired.length > 0 && (
            <div className="mb-4">
              <div className="flex items-center text-red-600 mb-2">
                <AlertTriangle className="w-5 h-5 mr-2" />
                <span className="font-medium">Vencidos ({expiringDocs.expired.length})</span>
              </div>
              {expiringDocs.expired.slice(0, 3).map((doc, idx) => (
                <div key={idx} className="text-sm text-gray-600 ml-7">
                  {doc.type} - Venció: {doc.expiry_date}
                </div>
              ))}
            </div>
          )}

          {expiringDocs.expiring_soon.length > 0 && (
            <div>
              <div className="flex items-center text-yellow-600 mb-2">
                <CheckCircle className="w-5 h-5 mr-2" />
                <span className="font-medium">Próximos a Vencer ({expiringDocs.expiring_soon.length})</span>
              </div>
              {expiringDocs.expiring_soon.slice(0, 3).map((doc, idx) => (
                <div key={idx} className="text-sm text-gray-600 ml-7">
                  {doc.type} - Vence: {doc.expiry_date}
                </div>
              ))}
            </div>
          )}

          {expiringDocs.expired.length === 0 && expiringDocs.expiring_soon.length === 0 && (
            <p className="text-gray-500 text-sm">No hay documentos próximos a vencer</p>
          )}
        </div>
      </div>

      {/* Vehicle Profitability Table */}
      <div className="bg-white rounded-lg shadow">
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-800">Top 5 Vehículos Más Rentables</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Patente</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Ingresos</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Gastos</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Neto</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {profitability.map((vehicle, idx) => (
                <tr key={idx} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {vehicle.license_plate}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-green-600">
                    ${vehicle.total_income.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-red-600">
                    ${vehicle.total_expenses.toFixed(2)}
                  </td>
                  <td className={`px-6 py-4 whitespace-nowrap text-sm text-right font-medium ${
                    vehicle.net_profit >= 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    ${vehicle.net_profit.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
