import { useState } from 'react';
import { Container, Card, Typography, TextField, Button, Alert, CircularProgress } from '@mui/material';
import api from '../api';

export default function UploadPoster() {
  const [file, setFile] = useState(null);
  const [formData, setFormData] = useState({ title: '', date: '', time: '', location: '', description: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

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
      setFormData(response.data); // предполагаем, что бэкенд возвращает заполненные поля
    } catch (err) {
      setError('Ошибка распознавания');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/admin/add_ticket', formData);
      alert('Событие добавлено');
    } catch (err) {
      setError('Ошибка сохранения');
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Card sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom>Добавление события</Typography>
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
          <Button type="submit" variant="contained" sx={{ mt: 2 }}>
            Сохранить событие
          </Button>
        </form>
      </Card>
    </Container>
  );
}