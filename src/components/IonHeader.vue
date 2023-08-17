<script setup lang="ts">
import { IonCol, IonGrid, IonHeader, IonRow, IonSearchbar, IonSelect, IonSelectOption, IonTitle, IonToolbar } from '@ionic/vue';
import { Ref, ref } from 'vue';

defineProps({
  search: {
    type: String,
    required: true
  }
})

function handleInput(event: CustomEvent) {
  // search.value = event.detail.value;
}
</script>

<template>
  <IonHeader>
    <IonToolbar>
      <IonGrid>
        <IonRow class="ion-align-items-center">
          <IonCol size-xs="5" size-sm="4" size-md="6" size-lg="6" size-xl="6">
            <IonTitle>
              <slot></slot>
            </IonTitle>
          </IonCol>
          <IonCol size-xs="7" size-sm="4" size-md="3" size-lg="3" size-xl="3">
            <IonSelect interface="popover" fill="outline" placeholder="Release Date">
              <IonSelectOption :value="0">Release Date</IonSelectOption>
              <IonSelectOption :value="1">Sort by price</IonSelectOption>
              <IonSelectOption :value="2">Sort by name</IonSelectOption>
            </IonSelect>
          </IonCol>
          <IonCol size-xs="12" size-sm="4" size-md="3" size-lg="3" size-xl="3">
            <IonSearchbar :animated="true" @ion-input="handleInput"></IonSearchbar>
          </IonCol>
        </IonRow>
      </IonGrid>
    </IonToolbar>
  </IonHeader>
</template>

<style scoped lang="scss">
ion-select {
  min-height: 42px;
}

ion-searchbar {
  text-align: left;
  height: 42px;
}

ion-title {
  height: 42px;
  padding-right: 0px;
}
</style>
