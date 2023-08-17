<script setup lang="ts">
import { ContentType } from '@/dto/content';
import { IonTabBar, IonTabButton, IonTabs, IonLabel, IonIcon, IonPage, IonRouterOutlet } from '@ionic/vue';
import { layersOutline, alertOutline, ribbonOutline, sparklesOutline } from 'ionicons/icons';

function icon(type: ContentType): string {
  switch (type) {
    case ContentType.Products:
      return layersOutline;
    case ContentType.Sales:
      return ribbonOutline;
    case ContentType.NewRelease:
      return alertOutline;
    case ContentType.PreOrder:
      return sparklesOutline;
  }
}
</script>

<template>
  <IonPage>
    <IonTabs>
      <IonRouterOutlet></IonRouterOutlet>
      <IonTabBar slot="bottom">
        <IonTabButton :tab="type" :href="type" v-for="type in Object.values(ContentType)">
          <IonIcon aria-hidden="true" :icon="icon(type)" />
          <IonLabel>{{ type }}</IonLabel>
        </IonTabButton>
      </IonTabBar>
    </IonTabs>
  </IonPage>
</template>
