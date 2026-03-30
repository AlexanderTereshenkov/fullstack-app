import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

// Страницы
import Login from './pages/Login';
import Register from './pages/Register';
import Events from './pages/Events';
import EventDetail from './pages/EventDetail';
import Profile from './pages/Profile';
import AdminProfile from './pages/AdminProfile';
import UploadPoster from './pages/UploadPoster';

// Компонент для защиты маршрутов
function PrivateRoute({ children, allowedRoles = [] }) {
  const user = JSON.parse(localStorage.getItem('user'));
  if (!user) return <Navigate to="/login" />;
  if (allowedRoles.length && !allowedRoles.includes(user.role)) {
    return <Navigate to="/" />;
  }
  return children;
}

const theme = createTheme();

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const stored = localStorage.getItem('user');
    if (stored) setUser(JSON.parse(stored));
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login setUser={setUser} />} />
          <Route path="/register" element={<Register />} />
          <Route path="/" element={<Events />} />
          <Route path="/events/:id" element={<EventDetail />} />
          <Route
            path="/profile"
            element={
              <PrivateRoute>
                <Profile user={user} />
              </PrivateRoute>
            }
          />
          <Route
            path="/admin/profile"
            element={
              <PrivateRoute allowedRoles={['admin']}>
                <AdminProfile user={user} />
              </PrivateRoute>
            }
          />
          <Route
            path="/admin/upload-poster"
            element={
              <PrivateRoute allowedRoles={['admin']}>
                <UploadPoster />
              </PrivateRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;