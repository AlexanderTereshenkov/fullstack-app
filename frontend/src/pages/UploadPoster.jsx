import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import {
  Container, Card, Typography, TextField, Button, CircularProgress, Alert, Box
} from '@mui/material';
import api from '../api';

export default function UploadPoster() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const eventId = searchParams.get('edit'); // получаем id из ?edit=13

  const [file, setFile] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    date: '',
    time: '',
    location: '',
    description: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [loadingEvent, setLoadingEvent] = useState(!!eventId);

  // Загрузка данных события при редактировании
  useEffect(() => {
    if (eventId) {
      const fetchEvent = async () => {
        try {
          const response = await api.get(`/events/${eventId}`);
          const event = response.data;
          // Предполагаем, что date приходит в формате ISO или строкой "YYYY-MM-DD HH:MM:SS"
          // Разделяем на дату и время
          let date = '';
          let time = '';
          if (event.date) {
            const dt = new Date(event.date);
            date = dt.toLocaleDateString('en-GB').replace(/\//g, '.');;
            time = dt.toTimeString().slice(0, 5);
          }
          setFormData({
            title: event.title || '',
            date,
            time,
            location: event.location || '',
            description: event.description || '',
          });
        } catch (err) {
          setError('Не удалось загрузить событие');
        } finally {
          setLoadingEvent(false);
        }
      };
      fetchEvent();
    }
  }, [eventId]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError('');
    const data = new FormData();
    data.append('file', file);
    try {
      const response = await api.post('/admin/ocr', data, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setFormData((prev) => ({ ...prev, ...response.data }));
    } catch (err) {
      setError('Ошибка распознавания');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      if (eventId) {
        // Редактирование
        await api.put(`/admin/update_event/${eventId}`, formData);
        alert('Событие обновлено');
      } else {
        // Создание
        await api.post('/admin/add_event', formData);
        alert('Событие добавлено');
      }
      navigate('/'); // или на страницу со списком событий
    } catch (err) {
      setError('Ошибка сохранения');
    } finally {
      setLoading(false);
    }
  };

  if (loadingEvent) {
    return (
      <Container sx={{ mt: 4, textAlign: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Card sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>
          {eventId ? 'Редактирование события' : 'Добавление события'}
        </Typography>

        <input type="file" accept="image/*" onChange={handleFileChange} />
        <Button onClick={handleUpload} disabled={!file || loading} sx={{ mt: 1 }}>
          {loading ? <CircularProgress size={24} /> : 'Распознать афишу'}
        </Button>

        {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}

        <form onSubmit={handleSubmit} style={{ marginTop: 20 }}>
          <TextField
            fullWidth
            label="Название"
            margin="normal"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            required
          />
          <TextField
            fullWidth
            label="Дата"
            margin="normal"
            value={formData.date}
            onChange={(e) => setFormData({ ...formData, date: e.target.value })}
            required
          />
          <TextField
            fullWidth
            label="Время"
            margin="normal"
            value={formData.time}
            onChange={(e) => setFormData({ ...formData, time: e.target.value })}
          />
          <TextField
            fullWidth
            label="Место"
            margin="normal"
            value={formData.location}
            onChange={(e) => setFormData({ ...formData, location: e.target.value })}
            required
          />
          <TextField
            fullWidth
            label="Описание"
            margin="normal"
            multiline
            rows={4}
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          />
          <Button
            type="submit"
            variant="contained"
            sx={{ mt: 2 }}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : (eventId ? 'Сохранить изменения' : 'Сохранить событие')}
          </Button>
        </form>
      </Card>
    </Container>
  );
}