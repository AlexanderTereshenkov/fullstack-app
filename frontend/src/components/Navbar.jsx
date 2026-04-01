import { AppBar, Toolbar, Button } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const userRole = localStorage.getItem('user');

  const handleProfileClick = () => {
    const targetPath = userRole === 'admin' ? '/admin/profile' : '/profile';
    if (location.pathname === targetPath) {
      return;
    }
    navigate(targetPath);
  };

  const handleLogout = () => {
    if (userRole) {
        if (location.pathname === '/login') {
            return;
        }
        navigate('/login');
        localStorage.clear();
    }
  }

  return (
    <AppBar position="static">
      <Toolbar>
        {!!userRole ? (
          <>
            <Button color="inherit" onClick={handleProfileClick}>
              Мой профиль
            </Button>
            <Button color="inherit" onClick={handleLogout}>
              Выйти
            </Button>
          </>
        ) : (
          <>
            <Button color="inherit" onClick={() => navigate('/login')}>
              Войти
            </Button>
            <Button color="inherit" onClick={() => navigate('/register')}>
              Регистрация
            </Button>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
}