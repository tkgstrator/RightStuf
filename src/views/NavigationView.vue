<template>
  <IonPage>
    <IonTabs>
      <IonRouterOutlet></IonRouterOutlet>
      <IonTabBar slot="bottom">
        <IonTabButton tab="/all" href="/">
          <IonIcon aria-hidden="true" :icon="triangle" />
          <IonLabel>Products</IonLabel>
        </IonTabButton>
        <IonTabButton tab="/pre-order" href="/pre-order">
          <IonIcon aria-hidden="true" :icon="triangle" />
          <IonLabel>Pre order</IonLabel>
        </IonTabButton>
        <IonTabButton tab="/new-release" href="/new-release">
          <IonIcon aria-hidden="true" :icon="triangle" />
          <IonLabel>New release</IonLabel>
        </IonTabButton>
        <IonTabButton tab="/sales" href="/sales">
          <IonIcon aria-hidden="true" :icon="triangle" />
          <IonLabel>Sales</IonLabel>
        </IonTabButton>
      </IonTabBar>
    </IonTabs>
  </IonPage>
</template>

<script setup lang="ts">
import { IonTabBar, IonTabButton, IonTabs, IonLabel, IonIcon, IonPage, IonRouterOutlet } from '@ionic/vue';
import { ellipse, square, triangle } from 'ionicons/icons';
</script>
