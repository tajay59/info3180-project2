<template>
      <footer class="mt-5">
          <div class="footer">
              <p>Copyright &copy {{ year }} United Auto Sales Inc.</p>
          </div>
      </footer>
</template>

<script>
export default {
    data() {
      return {
          year: (new Date).getFullYear()
      }        
    }
}
</script>

<style>
/* Add any component specific styles here */
footer{
    background-color: #232323;
    color: cornsilk;
    width: 100%; 
    font-size: 10px;
}
</style>