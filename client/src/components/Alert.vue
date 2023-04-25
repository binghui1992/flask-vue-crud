<template>
  <div>
    <!-- Alert component is from Bootstrap -->
    <div class="alert alert-success" role="alert">{{ message }}</div>
    <br/>
  </div>
</template>

<script>
export default ({
  props: ['message'],
});
</script>
