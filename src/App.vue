<template>
  <div id="app">
    <Header />
    <main>
      <router-view />
    </main>
    <Footer />
    <AIChat />
  </div>
</template>

<script>
import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
import AIChat from './components/AIChat.vue'

export default {
  name: 'App',
  components: {
    Header,
    Footer,
    AIChat
  }
}
</script>