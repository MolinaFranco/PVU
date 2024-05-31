Vue.component('pvu-button', {
  props: ['icon', 'url', 'disabled'],
  template: `
    <v-btn icon target="_blank" :href="url" :disabled="disabled">
      <v-icon>mdi-{{ icon }}</v-icon>
    </v-btn>
  `,
});

Vue.component('pvu-card', {
  props: ['title', 'color', 'img'],
  template: `
    <v-card :color="color" dark class="d-flex flex-column justify-space-between" style="height: 100%;" style="text-align: justify;">
      <v-container fluid class="pa-0 d-flex flex-column flex-grow-1">
        <v-row>
          <v-col>
            <v-card-title class="headline">{{ title }}</v-card-title>
            <v-card-subtitle style="margin-bottom: 32px;">
              <slot name="content"></slot>
            </v-card-subtitle>
          </v-col>
          <v-col cols="auto">
            <v-avatar class="ma-3 rounded" size="125" tile>
              <v-img :src="img"></v-img>
            </v-avatar>
          </v-col>
        </v-row>
      </v-container>
      <v-card-actions class="pa-4 d-flex justify-end">
        <slot name="buttons"></slot>
      </v-card-actions>
    </v-card>
  `,
});

Vue.component('pvu-div', {
  props: ['nCols', 'nRows'],
  data(instance) {
    return {
      defaultProps: {
        ...instance.$props,
      },
    };
  },
  methods: {
    onResize() {
      if (window.innerWidth < 600) {
        this.nCols = 1;
      } else {
        this.nCols = this.defaultProps.nCols;
      }
    },
  },
  created() {
    window.addEventListener('resize', this.onResize);
    this.onResize();
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.onResize);
  },
  computed: {
    style() {
      return {
        display: 'grid',
        gridTemplateColumns: `repeat(${this.nCols}, 1fr)`,
        gridAutoRows: 'auto',
        gridGap: '1rem',
        marginTop: '1rem',
      };
    },
  },
  template: `
    <div class="grid" :style="style">
      <slot></slot>
    </div>
  `,
});
