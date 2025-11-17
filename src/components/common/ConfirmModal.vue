<template>
  <div v-if="show" class="modal-overlay" @click.self="$emit('cancel')">
    <div class="confirm-modal">
      <div class="modal-icon" :class="type">
        <i :class="iconClass"></i>
      </div>
      
      <div class="modal-content">
        <h3>{{ title }}</h3>
        <p>{{ message }}</p>
      </div>
      
      <div class="modal-actions">
        <button 
          class="btn btn-outline" 
          @click="$emit('cancel')"
        >
          {{ cancelText }}
        </button>
        <button 
          class="btn" 
          :class="confirmButtonClass"
          @click="$emit('confirm')"
        >
          {{ confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfirmModal',
  props: {
    show: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: '确认操作'
    },
    message: {
      type: String,
      required: true
    },
    confirmText: {
      type: String,
      default: '确认'
    },
    cancelText: {
      type: String,
      default: '取消'
    },
    type: {
      type: String,
      default: 'info',
      validator: (value) => ['info', 'warning', 'danger', 'success'].includes(value)
    }
  },
  emits: ['confirm', 'cancel'],
  computed: {
    iconClass() {
      const icons = {
        info: 'fas fa-info-circle',
        warning: 'fas fa-exclamation-triangle',
        danger: 'fas fa-exclamation-circle',
        success: 'fas fa-check-circle'
      }
      return icons[this.type] || icons.info
    },
    confirmButtonClass() {
      return `btn-${this.type}`
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.confirm-modal {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  animation: modal-appear 0.3s ease;
}

@keyframes modal-appear {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 30px auto 20px;
  font-size: 1.8rem;
}

.modal-icon.info {
  background: rgba(0, 86, 210, 0.1);
  color: var(--primary);
}

.modal-icon.warning {
  background: rgba(255, 193, 7, 0.1);
  color: #ffc107;
}

.modal-icon.danger {
  background: rgba(220, 53, 69, 0.1);
  color: var(--danger);
}

.modal-icon.success {
  background: rgba(40, 167, 69, 0.1);
  color: var(--success);
}

.modal-content {
  padding: 0 30px 20px;
}

.modal-content h3 {
  margin: 0 0 10px 0;
  color: var(--text);
  font-size: 1.3rem;
  font-weight: 600;
}

.modal-content p {
  margin: 0;
  color: var(--text-light);
  line-height: 1.5;
  font-size: 0.95rem;
}

.modal-actions {
  display: flex;
  gap: 15px;
  padding: 20px 30px 30px;
  border-top: 1px solid var(--border);
}

.btn {
  flex: 1;
  padding: 12px 20px;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-outline {
  background: transparent;
  color: var(--text);
  border: 1px solid var(--border);
}

.btn-outline:hover {
  background: var(--secondary);
  border-color: var(--text-light);
}

.btn-info {
  background: var(--primary);
  color: white;
}

.btn-info:hover {
  background: #0046b8;
  transform: translateY(-1px);
}

.btn-warning {
  background: #ffc107;
  color: #212529;
}

.btn-warning:hover {
  background: #e0a800;
  transform: translateY(-1px);
}

.btn-danger {
  background: var(--danger);
  color: white;
}

.btn-danger:hover {
  background: #c82333;
  transform: translateY(-1px);
}

.btn-success {
  background: var(--success);
  color: white;
}

.btn-success:hover {
  background: #218838;
  transform: translateY(-1px);
}

@media (max-width: 480px) {
  .modal-actions {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
  }
}
</style>